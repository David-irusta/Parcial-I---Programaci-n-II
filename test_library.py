import unittest, os, tempfile, csv
from library import LibraryItem, Book, Magazine, load_library_items_from_csv, checkout_items, find_by_title, count_items

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.book = Book("Miguel de Cervantes", 350, 2, "Don Quijote", "David")
        self.magazine = Magazine("Magazine", 42, 2, "David")

    #Aqui probaremos constructores validos de la clase Libro
    def test_book(self):
        self.assertEqual(self.book.author, "Miguel de Cervantes")
        self.assertEqual(self.book.pages, 350)
        self.assertEqual(self.book.item_id, 2)
        self.assertEqual(self.book.title, "Don Quijote")
        self.assertEqual(self.book.user, "David")
    
    #Aqui probaremos constructores valido de la clase Magazine
    def test_magazine(self):
        self.assertEqual(self.magazine.issue_number, 42)
        self.assertEqual(self.magazine.title, "Magazine")
        self.assertEqual(self.magazine.item_id, 2)
        self.assertEqual(self.magazine.user, "David")

    #Aqui probaremos constructores no validos de la clase Libro
    def test_book_invalid(self):
        with self.assertRaises(ValueError):
            Book("Miguel de Cervantes", -350, 2, "Don Quijote", "David") #Pages siendo numero negativo
        with self.assertRaises(ValueError):
            Book("", 350, 2, "Don Quijote", "David") #Author vacio
        with self.assertRaises(ValueError):
            Book("Miguel de Cervantes", 350, 0, "Don Quijote", "David") #item_id = 0, que es un numero invalido
        with self.assertRaises(ValueError):
            Book("Miguel de Cervantes", 350, 0, " ", "David") #author solo con un espacio

    #Aqui probaremos constructores invalidos en clase Magazine
    def test_magazine_invalid(self):
        with self.assertRaises(ValueError):
            Magazine(-15, "Magazine", 2, "David") #Issue_number negativo
        with self.assertRaises(ValueError):
            Magazine(42, "", 2, "David") #Sin titulo
        with self.assertRaises(ValueError):
            Magazine(42, "Magazine", 0, "David") #Item_id nulo
        with self.assertRaises(ValueError):
            Magazine(None, "Magazine", 2, "David") # issue_number es None
            

    #Verificamos que el metodo checkout de la clase Libro funciona 
    def test_checkout_book(self):
        result = self.book.checkout()
        self.assertEqual(result, f"Book {self.book.title} checked out by {self.book.user}")
    
    #Verificamos que checkout de la clase Magazine funciona
    def test_checkout_magazine(self):
        result = self.magazine.checkout()
        self.assertEqual(result, f"Magazine {self.magazine.title} checked out by {self.magazine.user}")

    #Chequeamos la funcion con un csv temporal
    def test_load_library_items_from_csv(self):
        fname = "temp_biblio.csv"
        lines = [
            ["book","Jose Mauro de Vasconcelos", "150", "3", "Mi planta naranja Lima", "Cecilia"],
            ["magazine", "23", "Semana", "1", "Cris"],
            ["book","Jose Mauro de Vasconcelos", "-80", "3", "Mi planta naranja Lima", "Cecilia"], #Invalido: pages negativo
            ["magazine", "23", "Semana", "1", ""], #Usuario invalido
            ["unknown", "23", "Semana", "1", "Cris"], #Clase incorrecta
            [], #Vacia
            ["book", "Ana Frank", "376", "2", "El diario de Ana Frank", "Cecilia"]
        ]
        with open(fname, "w", newline="", encoding="utf-8")as f:
            writer = csv.writer(f)
            writer.writerows(lines)
        items = load_library_items_from_csv(fname)

        # 1) Compruebo el numero total de items
        self.assertEqual(len(items), 4)

        # 2) Extraigo libros y revistas
        magazine = [s for s in items if isinstance(s, Magazine)]
        book = [s for s in items if isinstance(s, Book)]
        self.assertTrue(all(isinstance(s, Magazine) for s in magazine))
        self.assertTrue(all(isinstance(s, Book) for s in book))

        # 3) Verifico los datos del primer libro y la primera revista
        self.assertEqual(book[0].author, "Jose Mauro de Vasconcelos")
        self.assertEqual(book[0].pages, 150)
        self.assertEqual(book[0].title, "Mi planta naranja Lima")
        self.assertEqual(book[0].user, "Cecilia")

        self.assertEqual(magazine[0].issue_number, 23)
        self.assertEqual(magazine[0].title, "Semana")
        self.assertEqual(magazine[0].user, "Cris")

        os.remove(fname)

    #Pruebo la funcion de checkout_items pasandole el libro y usuario
    def test_checkout_items_book(self):
        results = checkout_items(self.book, "David")
        self.assertEqual(results[0], "Book Don Quijote checked out by David")

    #Pruebo la funcion de checkout_items pasandole revista y usuario
    def test_checkout_items_magazine(self):
        results = checkout_items(self.magazine, "Cecilia")
        self.assertEqual(results[0], "Magazine Magazine checked out by Cecilia")

    #Pruebo la funcion de buscar por el titulo
    def test_find_by_title(self):
        items = [self.book, self.magazine] #Aqui asigno una variable que toma la cantidad de libros y revistas
        encontrados = find_by_title(items, "Don Quijote") #Uso la funcion para buscar el libro de Don Quijote
        self.assertEqual(len(encontrados), 1) #Recorre la lista que coincida con el titulo
        self.assertEqual(encontrados[0].title, "Don Quijote")
    
    #Pruebo la funcion de contar los items 
    def test_count_items(self):
        items = [self.book, self.magazine] #Asigno la variable que contiene todos los libros y revistas que las clases tienen
        count_item = count_items(items) #llamo a la funcion que se definio en library.py y le paso todos los items 
        self.assertEqual(count_item["books"], 1, "Debe haber 1 libro")#book deberia contener un solo libro
        self.assertEqual(count_item["magazines"], 1, "Debe haber 1 revista")
    
if __name__ == "__main__":
    unittest.main()
    