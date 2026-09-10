# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from models.student import Student
from models.person import Person
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

from models.teacher import Teacher


@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Person) -> int:
        """Crée en BD l'entité Person correspondant au étudiant student

        :param student: à créer sous forme d'entité Person en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """

        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO Person (first_name, last_name, age, address) VALUES (%s, %s, %s, %s)"

            try:
                cursor.execute(sql, (student.first_name, student.last_name, student.age, student.address))
                Dao.connection.commit()
                student_id = cursor.lastrowid
            except Dao.connection.IntegrityError:
                print("Course already exists!")
                student_id = 0
            except Dao.connection.DatabaseError as error:
                print(error)
                student_id = 0

            print("Record inserted successfully.")
        ...
        return student_id

    def read(self, id_person: int) -> Optional[Person]:
        """Renvoit le student correspondant à l'entité dont l'id est id_person
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Person]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM person INNER JOIN student ON person.id_person = student.id_person WHERE id_person=%s"
            cursor.execute(sql, (id_person,))
            record = cursor.fetchone()
        if record is not None:
            person = Teacher(record['first_name'], record['last_name'], record['age'])
            person.id = record['id_person']
        else:
            person = None

        return person

    def readall(self) -> list:
        """Renvoit les students correspondant à l'entité Student
           (ou None s'il n'a pu être trouvé)"""

        students: list = []

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM person INNER JOIN student ON person.id_person = student.id_person"
            cursor.execute(sql)
            record = cursor.fetchall()
        if record is not None:
            for row in record:
                students = Student(row['first_name'], row['last_name'], row['age'])
        else:
            students = None

        return students

    def update(self, student: Person) -> bool:
        """Met à jour en BD l'entité Person correspondant à student, pour y correspondre

        :param student: student déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        update_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "UPDATE person SET first_name = %s, last_name = %s, age = %s WHERE id_person = %s)"

            try:
                cursor.execute(sql, (student.first_name, student.last_name, student.age, student.id_person))
                Dao.connection.commit()
            except Dao.connection.IntegrityError:
                print("Student already exists!")
                update_boolean = False
            except Dao.connection.DatabaseError as error:
                print(error)
                update_boolean = False

        ...
        return update_boolean

    def delete(self, student: Person) -> bool:
        """Supprime en BD l'entité Person correspondant à student

        :param student: student dont l'entité Person correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        delete_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM person WHERE id_person = %s)"

            try:
                cursor.execute(sql, (student.id_person,))
                Dao.connection.commit()
            except Dao.connection.IntegrityError as error:
                print(error)
                delete_boolean = False

        ...
        return delete_boolean
