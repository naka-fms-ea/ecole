# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address correspondant au adresse address

        :param address: à créer sous forme d'entité address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """

        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO address (street, city, postal_code) VALUES (%s, %s, %s)"

            try:
                cursor.execute(sql, (address.street, address.city, address.postal_code))
                Dao.connection.commit()
                address_id = cursor.lastrowid
            except Dao.connection.IntegrityError:
                print("Address already exists!")
                address_id = 0
            except Dao.connection.DatabaseError as error:
                print(error)
                address_id = 0

        ...
        return address_id

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoit l'adresse correspondant à l'entité dont l'id est id_address
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address=%s"
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address

    def update(self, address: Address) -> None:
        """Met à jour en BD l'entité Address correspondant à address, pour y correspondre

                :param address: adresse déjà mis à jour en mémoire
                :return: True si la mise à jour a pu être réalisée
                """

        update_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "UPDATE address SET street = %s, city = %s, postal_code = %s WHERE id_address = %s)"

            try:
                cursor.execute(sql, (address.street, address.city, address.postal_code, address.id))
                Dao.connection.commit()
            except Dao.connection.IntegrityError:
                print("Address already exists!")
                update_boolean = False
            except Dao.connection.DatabaseError as error:
                print(error)
                update_boolean = False

        ...
        return update_boolean

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité Address correspondant à address

        :param address: adresse dont l'entité Address correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        delete_boolean = True

        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM address WHERE id_address = %s)"

            try:
                cursor.execute(sql, (address.id,))
                Dao.connection.commit()
            except Dao.connection.IntegrityError as error:
                print(error)
                delete_boolean = False

        ...
        return delete_boolean