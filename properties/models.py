from django.db import connection

class Connection:
    def __init__(self) -> None:
        self.cursor = connection.cursor()

    def execute(self, query, params=''):
        try:
            if params == '':
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, [params])
        except Exception as e:
            return None
        finally:
            self.cursor.close()
        return self.cursor.fetchall(), self.cursor.description


class PropertyModel(Connection):
    fields = ['direccion', 'ciudad', 'estado', 'precio_venta', 'descripción']

    def filters(self, filter):
        filter_valids = {'year': 'p.year','city': 'p.city', 'status': 's.name'}
        filters = [f'{filter_valids.get(_filter)}=("{value}")'.replace(' ', '') for _filter, value in filter.items() if _filter in filter_valids.keys()]
        clause_sql = ' AND '.join(filters)
        query_s = f"""SELECT p.address, p.city, s.name, p.price, p.description
                    FROM property p
                    INNER JOIN status_history sh ON p.id=sh.property_id
                    INNER JOIN status s ON s.id=sh.status_id 
                    WHERE sh.update_date IN(SELECT MAX(update_date) FROM status_history GROUP BY property_id) AND (status_id=3 OR status_id=4 OR status_id=5) AND {clause_sql}"""

        return self.pretty_data(self.execute(query_s))
        
    def last_status(self):
        query_s = """select p.address, p.city, s.name, p.price, p.description
                    from property p
                    inner join status_history sh on p.id = sh.property_id
                    inner join status s on s.id  = sh.status_id
                    where sh.update_date in (select max(update_date) from status_history group by property_id) and (status_id = 3 or status_id = 4 or status_id =5)"""
        return self.pretty_data(self.execute(query_s))
    
    def pretty_data(self, results):
        json_response = []
        if results is None:
            return None

        for result in results[0]:
            clen_data = [self.clean_string(s) for s in result]
            json_response.append(dict(zip(self.fields, clen_data)))
        return json_response

    def clean_string(self, string):
        return '' if string is None else string
        
