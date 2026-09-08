# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.student import Student
from models.person import Person
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


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

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
        else:
            course = None

        return course

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        update_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "UPDATE course SET name = %s WHERE id_course = %s)"

            try:
                cursor.execute(sql, (course.name, course.id))
                Dao.connection.commit()
            except Dao.connection.IntegrityError:
                print("Course already exists!")
                update_boolean = False
            except Dao.connection.DatabaseError as error:
                print(error)
                update_boolean = False

        ...
        return update_boolean

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        delete_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM course WHERE id_course = %s)"

            try:
                cursor.execute(sql, (course.id,))
                Dao.connection.commit()
            except Dao.connection.IntegrityError as error:
                print(error)
                delete_boolean = False

        ...
        return delete_boolean
