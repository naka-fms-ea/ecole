# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""

from models.teacher import Teacher
from models.person import Person
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher, person: Person) -> int:
        """Crée en BD l'entité Teacher correspondant à l'enseignant teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :param person: à créer sous forme d'entité Person en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """

        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO Person (first_name, last_name, age, address) VALUES (%s, %s, %s, %s)"

            try:
                cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.address))
                Dao.connection.commit()
                teacher_id = cursor.lastrowid
            except Dao.connection.IntegrityError:
                print("Teacher already exists!")
                teacher_id = 0
            except Dao.connection.DatabaseError as error:
                print(error)
                teacher_id = 0

            sqltest = "INSERT INTO Teacher (hiring_date, id_person) VALUES (%s, %s)"

            try:
                cursor.execute(sqltest, (teacher.hiring_date, teacher.id))
                Dao.connection.commit()
                teacher_id = cursor.lastrowid
            except Dao.connection.IntegrityError:
                print("Teacher already exists!")
                teacher_id = 0
            except Dao.connection.DatabaseError as error:
                print(error)
                teacher_id = 0

            print("Record inserted successfully.")
        ...
        return teacher_id

    def read(self, id_person: int) -> Optional[Person]:
        """Renvoit le teacher correspondant à l'entité dont l'id est id_person
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM person INNER JOIN teacher ON person.id_person = teacher.id_person WHERE id_person=%s"
            cursor.execute(sql, (id_person,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
            teacher.id = record['id_person']
        else:
            teacher = None

        return teacher

    def readall(self) -> list:
        """Renvoit les teachers correspondant à l'entité Teacher
           (ou None s'il n'a pu être trouvé)"""

        teachers: list = []

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM person INNER JOIN teacher ON person.id_person = teacher.id_person"
            cursor.execute(sql)
            record = cursor.fetchall()
        if record is not None:
            for row in record:
                teachers = Teacher(row['first_name'], row['last_name'], row['age'], row['hiring_date'])
        else:
            teachers = None

        return teachers

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre

        :param teacher: teacher déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        update_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "UPDATE person SET first_name = %s WHERE id_person = %s)"

            try:
                cursor.execute(sql, (teacher.first_name, teacher.id))
                Dao.connection.commit()
            except Dao.connection.IntegrityError:
                print("Teacher already exists!")
                update_boolean = False
            except Dao.connection.DatabaseError as error:
                print(error)
                update_boolean = False

        ...
        return update_boolean

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: teacher dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        delete_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM person WHERE id_person = %s)"

            try:
                cursor.execute(sql, (teacher.id,))
                Dao.connection.commit()
            except Dao.connection.IntegrityError as error:
                print(error)
                delete_boolean = False

        ...
        return delete_boolean
