# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """

        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO course (name, start_date, end_date) VALUES (%s, %s, %s)"

            try:
                cursor.execute(sql, (course.name, course.start_date, course.end_date))
                Dao.connection.commit()
                course_id = cursor.lastrowid
            except Dao.connection.IntegrityError:
                print("Course already exists!")
                course_id = 0
            except Dao.connection.DatabaseError as error:
                print(error)
                course_id = 0

            print("Record inserted successfully.")
        ...
        return course_id

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course INNER JOIN teacher ON course.id_teacher = teacher.id_teacher INNER JOIN person ON teacher.id_person = person.id_person WHERE id_course = %s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'], record['first_name'], record['last_name'])
            course.id = record['id_course']
        else:
            course = None

        return course

    def readall(self) -> list:
        """Renvoit les courses correspondant à l'entité Course
           (ou None s'il n'a pu être trouvé)"""

        courses: list = []

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course INNER JOIN teacher ON course.id_teacher = teacher.id_teacher INNER JOIN person ON teacher.id_person = person.id_person"
            cursor.execute(sql)
            record = cursor.fetchall()
        if record is not None:
            for row in record:
                courses = Course(row['name'], row['start_date'], row['end_date'], row['first_name'], row['last_name'])
        else:
            courses = None

        return courses

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        update_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "UPDATE course SET name = %s, star_date = %s, end_date = %s WHERE id_course = %s)"

            try:
                cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id))
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
