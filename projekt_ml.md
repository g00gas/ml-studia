### Sformułowanie problemu

Celem tego projektu jest stworzenie systemu rekomendacji filmowych
opartego na nauczaniu maszynowym. System ma na celu dostarczenie
użytkownikom spersonalizowanych rekomendacji odnośnie filmów którymi
mogą być zainteresowani. Opierać się to będzie na podstawie ich
wcześniejszych preferencji, ocen i oraz ocen osób o podobnych gustach.

System będzie oparty na technikach nauczania maszynowego takich jak:

1.  Filtr kolaboratywny jest to algorytm bazujący na interakcji między
    użytkownikami o podobnych gustach. To jest, jeżeli użytkownik A
    obejrzał Film X, Film Y i Film A, a użytkownik B obejrzał Film Film
    X, Film, Y i Film C to użytkownik C o podobnym profilu dostanie
    rekomendacje w postaci Filmu X i Y.

2.  Rekomendacja filmów na podstawie treści. Algorytm działa w taki
    sposób, że jeżeli użytkownik A obejrzy Film X, Y, Z o podobnych
    atrybutach, np. tagach: "dramat", "akcja", "wojna", to system
    zarekomenduje mu filmy które posiadają te tagi (ewentualnie pasujące
    tagi, które przekraczają założoną później wagę).

### Zestaw danych

1.  Zestaw danych filmowych zawierających różne informacje o filmach
    takie jak: gatunek, tytuł oraz tagi. Te dane są potrzebne do
    zrozumienia charakterystyki filmów celem umożliwienia algorytmowi
    zrozumienia zależności pomiędzy danymi produkcjami aby na podstawie
    ich cech tworzyć rekomendacje.

2.  Zestaw danych użytkowników zawierających informacje o tym jacy
    użytkownicy w jaki sposób ocenili dane filmy. Te dane są potrzebne
    do zrozumienia zależności między użytkownikami, określenia ich
    preferencji oraz zastosowania filtra kolaboratywnego. Pozwala to
    stworzyć profil danego użytkownika i określić go interesuje.

Zestaw który zostanie użyty do projektu to "MovieLens 25M Dataset",
który zawiera 25 milionów ocen i milion tagów zastosowanych do 62 000
filmów przez 162 000 użytkowników.

([[https://grouplens.org/datasets/movielens/]{.underline}](https://grouplens.org/datasets/movielens/))
zawiera rzeczy takie jak:

Liczba użytkowników: Zestaw MovieLens zawiera recenzje i oceny filmów
wystawione przez różnych użytkowników. Może to obejmować tysiące lub
nawet miliony różnych użytkowników.

Liczba filmów: Zbiór MovieLens zawiera różne filmy, dla których
użytkownicy wystawili oceny. Zazwyczaj obejmuje to setki, tysiące lub
nawet dziesiątki tysięcy filmów. Skala ocen: Skala ocen w MovieLens
zazwyczaj jest numeryczna, na przykład od 1 do 5 gwiazdek. Użytkownicy
mogą przyznawać filmy różnym ocenom w tej skali, gdzie 1 oznacza
najniższą ocenę, a 5 najwyższą.

Informacje dodatkowe: Oprócz ocen, zestaw danych MovieLens może zawierać
również dodatkowe informacje, takie jak tytuły filmów, rok produkcji,
gatunek, opisy, a czasem nawet informacje o aktorach i reżyserach.

### Oczekiwany efekt działania

#### Filtr kolaboracyjny

Oczekiwanym efektem działania funkcji dla filtra kolaboratywnego jest
zwrócenie listy rekomendacji filmów dla danego użytkownika o określonym
identyfikatorze \"user_id_to_find_recommendations_for\". Funkcja ta
wykorzystuje technikę filtrowania współpracującego opartą na
użytkownikach, aby znaleźć innych użytkowników o podobnych gustach
filmowych, a następnie sugeruje filmy, które są najczęściej lub najwyżej
oceniane przez tych podobnych użytkowników.

Wynik działania funkcji to lista filmów, które reprezentują najlepsze
rekomendacje dla danego użytkownika. Liczba filmów w tej liście jest
ograniczona przez parametr \"top_recommendations\", który określa ilość
filmów, jakie zostaną zwrócone jako rekomendacje.

Dzięki filtrowaniu współpracującemu opartemu na użytkownikach, funkcja
ta pozwala na personalizowane rekomendacje, uwzględniając preferencje
użytkownika oraz opinie innych użytkowników o podobnych
zainteresowaniach. Efektem działania tej funkcji jest więc zbiór filmów,
które mają duże szanse zainteresować danego użytkownika na podstawie
ocen i preferencji innych użytkowników o zbliżonych gustach filmowych.

#### Filtr na podstawie treści

Oczekiwanym efektem działania funkcji
\"content_based_recommendation_system\" jest zwrócenie spersonalizowanej
listy rekomendacji filmów dla zadanego filmu o tytule
\"movie_title_to_find_recommendations_for\". Funkcja opiera się na
analizie cech filmów, takich jak tytuły i gatunki, aby znaleźć filmy o
podobnej tematyce lub gatunkach do filmu podanego jako wejście.

Dla danego filmu \"movie_title_to_find_recommendations_for\", funkcja
wykorzystuje dane zawarte w pliku \"movies.csv\", zawierającym
informacje o wielu filmach, w tym ich tytuły i gatunki. Na podstawie
tytułów i gatunków filmów, funkcja oblicza podobieństwo między filmami
za pomocą metody TF-IDF (Term Frequency-Inverse Document Frequency) oraz
podobieństwo kosinusowe.

Ostatecznie, funkcja zwraca listę filmów, które są najbardziej zbliżone
do zadanego filmu pod względem treści (tytułów i gatunków). Ta
spersonalizowana lista rekomendacji pozwala użytkownikowi odkrywać nowe
filmy o podobnej tematyce lub gatunkach do filmów, które go interesują.

Dzięki temu użytkownik może rozszerzyć swoje horyzonty filmowe i odkryć
produkcje, które byłyby mu wcześniej nieznane, ale które mają duże
szanse spodobać się na podstawie preferencji wyrażonych przez podobne
filmy. Efektem działania tej funkcji jest zatem usprawnienie procesu
rekomendacji filmów i dostarczenie użytkownikowi spersonalizowanej listy
propozycji, które odpowiadają jego zainteresowaniom filmowym.

### Wytłumaczenie algorytmów

#### Algorytm k- najbliższych sąsiadów

Algorytm filtracji współpracującej (k-najbliższych sąsiadów) to technika
rekomendacji, która opiera się na znajdowaniu \"k\" najbardziej
podobnych użytkowników lub elementów do danego użytkownika lub elementu.
Podobieństwo między użytkownikami lub elementami jest mierzone za pomocą
odległości kosinusowej, która ocenia kąt pomiędzy wektorami ocen
użytkowników lub cechami elementów.

Krótka ilustracja działania algorytmu:

1\. Przygotowanie danych: Dane dotyczące ocen filmów wystawionych przez
użytkowników są wczytywane i przygotowywane do analizy.

2\. Obliczenie odległości kosinusowej: Algorytm oblicza miarę
podobieństwa między użytkownikami lub elementami na podstawie odległości
kosinusowej. Ta metoda mierzy kąt między wektorami ocen użytkowników lub
cechami filmów, gdzie mniejszy kąt oznacza większe podobieństwo.

3\. Wybór \"k\" najbliższych sąsiadów: Algorytm wybiera \"k\"
użytkowników lub elementów o najmniejszej odległości kosinusowej do
danego użytkownika lub elementu.

4\. Wygenerowanie rekomendacji: Na podstawie preferencji tych \"k\"
najbliższych sąsiadów, algorytm generuje rekomendacje dla danego
użytkownika lub elementu. Na przykład, w przypadku rekomendacji filmów,
rekomendowane są filmy, które były dobrze ocenione przez tych podobnych
użytkowników.

Algorytm ten jest prosty w implementacji i efektywny dla dużej liczby
użytkowników lub elementów. Jednak może napotkać problemy, gdy brakuje
danych dla nowych użytkowników lub elementów, znane jako problem zimnego
startu (cold-start). Aby poprawić trafność rekomendacji, często
wykorzystuje się podejście hybrydowe, które łączy różne metody
rekomendacji, biorąc pod uwagę zarówno filtrowanie współpracujące, jak i
inne informacje, np. filtrowanie oparte na treściach czy demograficzne
dane użytkowników.

#### Macierz TF-IDF: 

Macierz TF-IDF jest narzędziem stosowanym w analizie tekstowej do oceny
ważności słów w kontekście dokumentów w zbiorze tekstów. W przypadku tej
funkcji, dokumentami są tytuły filmów i gatunki filmów. Proces tworzenia
macierzy TF-IDF polega na przypisaniu każdemu słowu (tutaj: słowom w
tytułach filmów i gatunkach) liczby reprezentującej, jak często
występuje w danym dokumencie (filmie). Jednocześnie redukuje się wagę
słów, które występują w wielu dokumentach, aby uniknąć dominacji słów
powszechnych. Ostatecznie, macierz TF-IDF reprezentuje dokumenty (tytuły
filmów i gatunki) jako wektory numeryczne, które są używane do
obliczania podobieństwa między dokumentami.

#### Podobieństwo kosinusowe:

Podobieństwo kosinusowe jest miarą podobieństwa między dwoma wektorami w
wielowymiarowej przestrzeni. W tym przypadku, każdy film jest
reprezentowany przez dwa wektory: wektor opisujący tytuł filmu oraz
wektor opisujący gatunki filmu. Podobieństwo kosinusowe jest obliczane,
aby ocenić, jak bardzo te wektory są zgodne, czyli jak bardzo tytuły i
gatunki filmów są podobne między sobą.

Wartość podobieństwa kosinusowego mieści się w zakresie od -1 do 1. Im
bliżej wartości do 1, tym większe podobieństwo między dwoma wektorami
(większy kąt między nimi). Wartość 1 oznacza, że wektory są identyczne.
Wartość -1 oznacza, że wektory mają przeciwny kierunek. Wartość bliska 0
oznacza, że wektory są prawie prostopadłe i mają niewielkie
podobieństwo.

### Stos technologiczny

Do nauczania maszynowego użyto:\
paczki scikit-learn, która pozwala na używanie macierzy TF-IDF,
podobieństwa kosinusowego i algorytmu najbliższych sąsiadów; pandas,
która pozwala na sprasowanie danych do użytecznych tabel.

Do wizualizacji danych użyto:

paczki matplotlib, która pozwala na tworzenie grafów; wordcloud do
wygenerowania chmury tagów, seaborn do tworzenia bardziej zaawansowanych
grafów.

Do stworzenia frontendu pokazującego aplikację użyto:\
Typescript dla mocnego typowania JavaScripta; React dla łatwego i
szybkiego tworzenia aplikacji internetowych; Vite dla użycia szybkiego
runnera dla projektów JS oraz serwera aplikacji.

Do stworzenia backendu pokazującego aplikację użyto:

Frameworku backendowego w Pythonie Flask, paczki psycoppg2 użytej do
połączenia z bazą postgres w której są trzymane dane odnośnie filmów.

Do stworzenia infrastruktury użyto:

Dockera, który pozwala skonteneryzować frontend, backend i bazę danych
celem szybkiego uruchomienia sklonowanego projektu.

PostgresSQL do przechowywania danych.
