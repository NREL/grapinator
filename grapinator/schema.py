from sqlalchemy import and_, or_, desc, asc
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import datetime
from grapinator import log, schema_settings
from grapinator.model import *

def gql_class_constructor(clazz_name, db_clazz_name, clazz_attrs, default_sort_col):
    gql_attrs = {
        'Meta': type('Meta', (), {'model': globals()[db_clazz_name], 'interfaces': (relay.Node, )})
        ,'matches': graphene.String(description='contains, exact, eq, gt, gte, lt, lte, ne', default_value='contains')
        ,'sort_by': graphene.String(description='Field to sort by.', default_value=default_sort_col)
        ,'logic': graphene.String(description='and, or', default_value='and')
        ,'sort_dir': graphene.String(description='asc, desc', default_value='asc')
        }

    for attr in clazz_attrs:
        gql_attrs[attr['name']] = attr['type'](attr['type_args'], description=attr['desc'])
    
    return type(str(clazz_name), (SQLAlchemyObjectType,), gql_attrs)

def gql_connection_class_constructor(clazz_name, gql_clazz_name):
    gql_attrs = {
        'Meta': type('Meta', (), {'node': gql_clazz_name})
        }
    return type(str(clazz_name), (relay.Connection,), gql_attrs)

class MyConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ['first', 'last', 'before', 'after']
    
    @classmethod
    def get_query(cls, model, info, **args):
        matches = None
        operator = None
        sort_by = None
        sort_dir = None
        filter_conditions = []
        if 'matches' in args:
            matches = args['matches']
            del args['matches']
        if 'logic' in args:
            operator = args['logic']
            del args['logic']
        if 'sort_by' in args:
            sort_by = getattr(model, args['sort_by']).name
            del args['sort_by']
        if 'sort_dir' in args:
            sort_dir = args['sort_dir']
            del args['sort_dir']
        sort = asc(sort_by) if sort_dir == "asc" else desc(sort_by)
        query = super(MyConnectionField, cls).get_query(model, info, **args)
        
        for field, value in args.items():
            if field not in cls.RELAY_ARGS:
                if matches == 'exact' or matches == 'eq':
                    filter_conditions.append(getattr(model, field) == value)
                elif matches == 'lt':
                    filter_conditions.append(getattr(model, field) < value)
                elif matches == 'lte':
                    filter_conditions.append(getattr(model, field) <= value)
                elif matches == 'gt':
                    filter_conditions.append(getattr(model, field) > value)
                elif matches == 'gte':
                    filter_conditions.append(getattr(model, field) >= value)
                elif matches == 'ne':
                    filter_conditions.append(getattr(model, field) != value)
                # these last 2 are opinionated defaults for searching date types and strings.
                elif isinstance(value, (datetime.date, datetime.datetime)):
                    filter_conditions.append(getattr(model, field) >= value)
                else: 
                    filter_conditions.append(getattr(model, field).ilike('%' + value + '%'))
        
        if operator == 'or':
            query = query.filter(or_(*filter_conditions)).order_by(sort)
        else:
            query = query.filter(and_(*filter_conditions)).order_by(sort)

        return query

# loop and dynamicaly create all the graphene classes necessary for the Query class
for clazz in schema_settings.get_gql_classes():
    # create the Graphene classes
    globals()[clazz['gql_class']] = gql_class_constructor(
        clazz['gql_class']
        ,clazz['gql_db_class']
        ,clazz['gql_columns']
        ,clazz['gql_db_default_sort_col']
        )

    # create the Graphene connection class
    """     
    globals()[clazz['gql_conn_class']] = gql_connection_class_constructor(
        clazz['gql_conn_class']
        ,globals()[clazz['gql_class']]
        ) 
    """

def _make_gql_query_fields(cols):
    gql_attrs = {}
    for row in cols:
        # Only allow queryable types. 
        # set optional 'gql_isqueryable': False in schema.dct to skip
        if row['isqueryable']:
            gql_attrs[row['name']] = row['type']()
    gql_attrs.update({
        'matches': graphene.String()
        ,'sort_by': graphene.String()
        ,'logic': graphene.String()
        ,'sort_dir': graphene.String()
        })
    return gql_attrs
    
# create the Graphene Query class
class Query(graphene.ObjectType):
    node = relay.Node.Field()

    for clazz in schema_settings.get_gql_classes():
        locals()[clazz['gql_conn_query_name']] = MyConnectionField(
            globals()[clazz['gql_class']]
            ,_make_gql_query_fields(clazz['gql_columns'])
            )

# create the gql schema
gql_schema = graphene.Schema(query=Query, auto_camelcase=False)