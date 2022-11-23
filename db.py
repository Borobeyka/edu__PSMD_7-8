from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

class DB():
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor(cursor_factory=RealDictCursor)

    def get_tasks_report(self, first_date, second_date):
        self.cursor.execute("SELECT t.*, ea.name author_name, ea.surname author_surname, ee.name executor_name, \
            ee.surname executor_surname, cl.name client_name, cl.surname client_surname, tp.priority task_priority, \
            c.description contract_description, ct.type contract_type, tt.type task_type FROM tasks t LEFT JOIN employees ea ON \
            ea.id = t.author_id LEFT JOIN employees ee ON ee.id = t.executor_id LEFT JOIN clients cl ON \
            cl.id = t.client_id LEFT JOIN tasks_priority tp ON tp.id = t.priority_id LEFT JOIN contracts c ON \
            c.id = t.contract_id LEFT JOIN contracts_type ct ON ct.id = c.type_id LEFT JOIN tasks_type tt ON \
            tt.id = t.type_id WHERE t.start_date >= %s or t.expire_date <= %s", (first_date, second_date))
        response = self.cursor.fetchall()
        if not response:
            return False
        return response

    def task_create(self, data, author_id):
        self.cursor.execute("INSERT INTO tasks VALUES (DEFAULT, %s, NOW(), DEFAULT, %s, %s, %s, %s, %s, %s, NULL, DEFAULT);", \
            (data.get("title").data, data.get("planned_date").data, author_id, data.get("executor_id").data, \
            data.get("client_id").data, data.get("priority_id").data, data.get("type_id").data))
        self.db.commit()
        self.cursor.execute("SELECT lastval()")
        return self.cursor.fetchone().get("lastval")
    
    def task_finish(self, task):
        self.cursor.execute("UPDATE tasks SET completed=true WHERE id=%s", (task.get("id"),))
        self.db.commit()
    
    def update_task(self, task_id, data):
        self.cursor.execute("UPDATE tasks SET title=%s, start_date=%s, planned_date=%s, executor_id=%s, priority_id=%s, type_id=%s WHERE id=%s", \
            (data.get("title").data, data.get("start_date").data, data.get("planned_date").data, data.get("executor_id").data, \
            data.get("priority_id").data, data.get("type_id").data, task_id))
        self.db.commit()
    
    def get_all_task_types(self):
        self.cursor.execute("SELECT id, type FROM tasks_type")
        response = self.cursor.fetchall()
        if not response:
            return False
        return response
        
    def get_all_employees(self):
        self.cursor.execute("SELECT id, name, surname FROM employees")
        response = self.cursor.fetchall()
        if not response:
            return False
        return response
    
    def get_all_task_priority(self):
        self.cursor.execute("SELECT id, priority FROM tasks_priority")
        response = self.cursor.fetchall()
        if not response:
            return False
        return response

    def get_all_clients(self):
        self.cursor.execute("SELECT id, name, surname FROM clients")
        response = self.cursor.fetchall()
        if not response:
            return False
        return response

    def get_user_tasks(self, user_id):
        self.cursor.execute("SELECT id, title, completed FROM tasks WHERE executor_id = %s OR author_id = %s", (user_id, user_id))
        response = self.cursor.fetchall()
        if not response:
            return False
        return response
    
    def get_user_task_by_id(self, user_id, task_id):
        self.cursor.execute("SELECT t.*, ea.name author_name, ea.surname author_surname, ee.name executor_name, \
            ee.surname executor_surname, cl.name client_name, cl.surname client_surname, tp.priority task_priority, \
            c.description contract_description, ct.type contract_type, tt.type task_type FROM tasks t LEFT JOIN employees ea ON \
            ea.id = t.author_id LEFT JOIN employees ee ON ee.id = t.executor_id LEFT JOIN clients cl ON \
            cl.id = t.client_id LEFT JOIN tasks_priority tp ON tp.id = t.priority_id LEFT JOIN contracts c ON \
            c.id = t.contract_id LEFT JOIN contracts_type ct ON ct.id = c.type_id LEFT JOIN tasks_type tt ON \
            tt.id = t.type_id WHERE (t.executor_id = %s OR t.author_id = %s) AND t.id = %s", \
            (user_id, user_id, task_id))
        response = self.cursor.fetchone()
        if not response:
            return False
        return response
    
    def get_user(self, user_id):
        self.cursor.execute("SELECT e.*, er.title as role_title FROM employees e LEFT JOIN employees_roles er ON er.id = e.role_id WHERE e.id = 1", \
            (user_id,))
        response = self.cursor.fetchone()
        if not response:
            return False
        return response

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM employees WHERE email = %s", (email,))
        response = self.cursor.fetchone()
        if not response:
            return False
        return response
    
    def register_user(self, data):
        self.cursor.execute("INSERT INTO employees VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (data.get("name").data, data.get("surname").data, data.get("phone").data, data.get("email").data, \
            data.get("address").data, data.get("company").data, data.get("role").data, generate_password_hash(data.get("pswd").data)))
        self.db.commit()