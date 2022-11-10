import pymysql

import os


class ContactResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        user = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        host = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=user,
            password=pw,
            host=host,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):
        '''
            select "email" as type,email as contact,kind from emails
            where uid = "xxx123"
            UNION
            select "phone", phone,kind from phones
            where uid = "xxx123"
            UNION
            select "address", address,kind from addresses
            where uid = "xxx123"
        '''
        sql = "SELECT 'email' as type, email as contact, kind FROM f22_contact_databases.emails where uid=%s UNION SELECT 'phone', phone, kind FROM f22_contact_databases.phones where uid=%s UNION SELECT 'address', address, kind FROM f22_contact_databases.addresses where uid=%s"
        conn = ContactResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=(key,key,key))
        result = cur.fetchall()

        return result
    
    @staticmethod
    def get_by_query(queryString, offset, limit):
        '''
            select "email" as type,email as contact,kind from emails
            where email like "%xx123%"
            UNION
            select "phone", phone,kind from phones
            where phone like "%xx123%"
            UNION
            select "address", address,kind from addresses
            where address like "%xx123%"
        '''
        q = '%'+queryString+'%'
        sql = "SELECT 'email' as type, email as contact, kind FROM f22_contact_databases.emails where email LIKE %s UNION SELECT 'phone', phone, kind FROM f22_contact_databases.phones where phone LIKE %s UNION SELECT 'address', address, kind FROM f22_contact_databases.addresses where address LIKE %s"
        conn = ContactResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=(q,q,q))
        result = cur.fetchall()

        ret = result[0:len(result)]
        if len(result) > offset:
            ret = ret[offset:len(ret)]

        if len(ret) > limit:
            ret = ret[0:limit]

        return ret

    @staticmethod
    def create_by_key(uid, type, contact, kind):
        conn = ContactResource._get_connection()
        cur = conn.cursor()

        sql = "INSERT IGNORE INTO f22_contact_databases.contacts (uid) VALUES (%s)"
        val = (uid)
        cur.execute(sql, val)

        # if type == "email": 
        #     sql = "SELECT email FROM f22_contact_databases.emails where uid=%s and kind=%s"
        #     res = cur.execute(sql, args=(uid,kind))
        #     result = cur.fetchall()
        #     if(len(result) > 0):
        #         return kind+" email already existed"
        #     sql = "INSERT INTO f22_contact_databases.emails (email, kind, uid) VALUES (%s,%s,%s)"
        # elif type == "phone": 
        #     sql = "SELECT phone FROM f22_contact_databases.phones where uid=%s and kind=%s"
        #     res = cur.execute(sql, args=(uid,kind))
        #     result = cur.fetchall()
        #     if(len(result) > 0):
        #         return kind+" phone already existed"
        #     sql = "INSERT INTO f22_contact_databases.phones (phone, kind, uid) VALUES (%s,%s,%s)"
        # else:
        #     sql = "SELECT address FROM f22_contact_databases.addresses where uid=%s and kind=%s"
        #     res = cur.execute(sql, args=(uid,kind))
        #     result = cur.fetchall()
        #     if(len(result) > 0):
        #         return kind+" addresses already existed"
        #     sql = "INSERT INTO f22_contact_databases.addresses (address, kind, uid) VALUES (%s,%s,%s)"
        sql = "SELECT "+type+" FROM f22_contact_databases."+type+"s where uid=%s and kind=%s"
        res = cur.execute(sql, args=(uid,kind))
        result = cur.fetchall()
        if(len(result) > 0):
            return kind+" "+type+" already existed"
        
        sql = "INSERT INTO f22_contact_databases."+type+"s ("+type+", kind, uid) VALUES (%s,%s,%s)"
        val = (contact, kind, uid)
        res = cur.execute(sql, val)

        if res > 0:
                return "success"
        else:
            return "fail"

    @staticmethod
    def update_by_key(uid, type, contact, kind):
        conn = ContactResource._get_connection()
        cur = conn.cursor()

        sql = "SELECT uid FROM f22_contact_databases.contacts where uid=%s"
        res = cur.execute(sql, args=(uid))
        result = cur.fetchall()
        if len(result) <= 0:
            return "user doesn't exist"
        
        sql = "UPDATE f22_contact_databases."+type+"s SET "+type+" = %s WHERE kind = %s AND uid = %s"
        val = (contact, kind, uid)
        cur.execute(sql, val)

        if cur.rowcount > 0:
                return "success"
        else:
            return "fail"
    
    @staticmethod
    def delete_by_key(uid, type, kind):
        conn = ContactResource._get_connection()
        cur = conn.cursor()
    
        sql = "SELECT uid FROM f22_contact_databases.contacts where uid=%s"
        res = cur.execute(sql, args=(uid))
        result = cur.fetchall()
        if len(result) <= 0:
            return "user doesn't exist"
        
        sql = "DELETE FROM f22_contact_databases."+type+"s WHERE kind = %s and uid = %s"
        val = (kind, uid)
        cur.execute(sql, val)
        
        if cur.rowcount > 0:
                return "success"
        else:
            return "fail"
    

