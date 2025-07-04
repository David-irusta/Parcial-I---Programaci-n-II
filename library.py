from abc import ABC, abstractmethod
import csv

#Creamos la clase abstracta LibraryItem
class LibraryItem(ABC):
    def __init__(self, title: str, item_id: int):
        self.title = title
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Debe tener un titulo")
        self.item_id = item_id
        if not isinstance(item_id, int) or item_id <= 0:
            raise ValueError("Debe tener un id valido")
    
    @abstractmethod
    def checkout(self, user: str) -> str:
        self.user = user
        pass

#Crear la clase hija Book
class Book(LibraryItem):
    def __init__(self, author: str, pages: int, item_id: int, title: str, user: str):
        super().__init__(title, item_id)
        self.author = author
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Tiene que escribir algo")
        self.pages = pages
        if not isinstance(pages, int) or pages <= 0:
            raise ValueError("La pagina debe ser un numero valido")
        self.user = user
        if not isinstance(user, str) or not user.strip():
            raise ValueError("Usuario invalido")
        
    #Le damos el metodo abstracto checkout
    def checkout(self) -> str:
        return f"Book {self.title} checked out by {self.user}"
    
#Creamos la clase Magazine        
class Magazine(LibraryItem):
    def __init__(self, title: str, issue_number: int, item_id: int, user: str):
        super().__init__(title, item_id)
        self.issue_number = issue_number
        if not isinstance(issue_number, int) or issue_number <= 0:
            raise ValueError("La edicion debe ser un numero valido")
        self.user = user
        if not isinstance(user, str) or not user.strip:
            raise ValueError("Usuario no valido")
    
    #Y le pasamos el metodo abstracto checkout
    def checkout(self,) -> str:
        return(f"Magazine {self.title} checked out by {self.user}")

#Creamos la primera funcion que crea listas de items y errores    
def load_library_items_from_csv(path: str) -> list[LibraryItem]:
    items = []  #Aqui los items (libros y revistas) que se van agregando al archivo temporal csv
    errors = [] #Registramos los errores 
    with open(path, "r", newline= "") as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader, start = 1): #Recorremos por fila y enumeramos 
            if not row:
                continue #Si tal fila no existe, continua
            Litem_type = row[0].strip().lower() 
            try:
                if Litem_type == "book":
                    if len(row) != 6:
                        raise ValueError("Libro espera 5 argumentos") #Si "Book" tiene mas de 5 argumentos lanza error de valor
                    author = row[1] #Le pasamos el orden de los argumentos por cada lugar de la fila, en este caso es 1
                    pages = int(row[2])
                    item_id = int(row[3])
                    title = row[4]
                    user = row[5]
                    items.append(Book(author, pages, item_id, title, user)) #Agrega el item
                elif Litem_type == "magazine":
                    if len(row) != 5:
                        raise ValueError("Revista espera 4 argumentos") #repetimos pero con clase Magazine
                    issue_number = int(row[1]) 
                    title = row[2]
                    item_id = int(row[3])
                    user = row[4]
                    items.append(Magazine(title, issue_number, item_id, user))
            except Exception as e:
                print(f"{index} - Error: {e}")
                errors.append(f"{index} - Error: {e}") #Lanza una excepcion y notifica
    return items

#Funcion para checkear los items
def checkout_items(items: list[LibraryItem], user: str) -> list[str]:
    if not isinstance(items, list): #Si no es instancia  de items
        items = [items]
    results = []
    for item in items:
        try:
            item.user = user
            results.append(item.checkout()) #Agrega un resultado checkeando el item 
        except Exception as e:
            results.append(f"Error salida: {e}") #
    return results

def count_items(items: list[LibraryItem]) -> dict:
    contar = {
        "books": 0,
        "magazines": 0
    }
    for item in items:
        if isinstance(item, Book):
            contar["books"] += 1
        elif isinstance(item, Magazine):
            contar["magazines"] += 1
    return contar

def find_by_title(items: list[LibraryItem], keyword: str) -> list[LibraryItem]:
    encontrar_item = []
    for item in items:
        if keyword.lower() in item.title.lower():
            encontrar_item.append(item)
    return encontrar_item


revista = Magazine("Rolling Stone", 42, 1, "David")
Libro = Book("Miguel de Cervantes", 350, 2, "Don Quijote", "David")
print(Libro.checkout())
print(revista.checkout())