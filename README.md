Nowoczesne Technologie Przetwarzania Danych


Lab 13


Temat: Orkiestracja kontenerów w Kubernetes - wdrożenie API modelu ML na lokalnym klastrze


Dominika Liszkiewicz


Zadanie 1 


Sposób uruchomienia klastra:


Lokalny klaster Kubernetes został  uruchomiony przy użyciu środowiska wbudowanego bezpośrednio w aplikację Docker Desktop.


Wersje oprogramowania:



- Wersja klienta (Client Version): v1.34.1

  
- Wersja serwera (Server Version): v1.34.1

  
- Wersja Kustomize: v5.7.1
  

  <img width="1430" height="638" alt="image (71)" src="https://github.com/user-attachments/assets/d6d7a0da-aeda-4ea7-a241-49b24348b3a1" />


Zadanie 2  


Nazwa: ml-api


Tag obrazu: 1.0


<img width="1426" height="1132" alt="image (72)" src="https://github.com/user-attachments/assets/021c6349-ea01-489b-b5aa-3a07c7cb2fe6" />



Zadanie 3 


<img width="1410" height="980" alt="image (73)" src="https://github.com/user-attachments/assets/2e11b746-2035-45b0-8c4f-424b0b099936" />


Zadanie 4 


<img width="1426" height="830" alt="image (74)" src="https://github.com/user-attachments/assets/8d7cf72f-5f4b-4489-a66b-cfec5a0cdea8" />


Najpierw przeskalowałam aplikację do 4 replik i pomyślnie się uruchomiły. Potem usunęłam jeden pod. Usunięty pod zniknął, ale na jego miejsce wskoczył nowy pod o innej nazwie. 


<img width="1408" height="1364" alt="image (75)" src="https://github.com/user-attachments/assets/544953fc-1e85-4bb1-a59a-e5f605a8bf51" />


Logi z ciągłego odpytywania endpointu podczas rolling update. Widać moment przełączenia pomiędzy wersjami kontenerów i automatyczne wznowienie ruchu przez nowy pod.  


<img width="1414" height="626" alt="image (76)" src="https://github.com/user-attachments/assets/51869888-0184-451e-8490-e88ac2c93daf" />


Aktualizacja do wersji 2.0 się udała, rollback zadziała poprawnie. 


Podczas skalowania klaster wysłał żądanie utworzenia dwóch nowych podów o losowo wygenerowanych nazwach końcowych. Pody przeszły w status ContainerCreating. Kontenery FastAPI w nowych podach wystartowały i po około 5 sekundach pody zmieniły status na Running. Usługa sieciowa (Service) automatycznie wykryła nowe pody i zaczęła kierować do nich część ruchu (od teraz zapytania z pętli były dzielone na 4 pody zamiast na 2).


Podczas aktualizacji Kubernetes nie wyłączył od razu starych podów. Zamiast tego stworzył nowy pod z obrazem w wersji 2.0. Klaster czekał, aż nowy pod przejdzie w status Running. Gdy pierwszy nowy pod (2.0) był gotowy do pracy, usługa sieciowa zaczęła kierować do niego zapytania. W tym samym momencie Kubernetes wydał rozkaz usunięcia jednego ze starych podów (1.0), który przeszedł w status Terminating. 


Zadanie 5 


Sondy readiness poprawnie weryfikują stan kontenera


<img width="1412" height="234" alt="image (77)" src="https://github.com/user-attachments/assets/4c4dbb46-d04c-46cd-8854-4999c612160f" />


Liczba podów zmienia się pod obciążeniem


<img width="1414" height="306" alt="image (78)" src="https://github.com/user-attachments/assets/e02e31fb-9f7e-480d-b6ef-69ae1814c612" />


Pojedynczy kontener Docker - jest to wyizolowany proces na jednym węźle, jeśli proces wewnątrz kontenera ulegnie awarii - kontener przestaje działać i aplikacja jest niedostępna 


Wdrożenie w Kubernetes - służy do zarządzania grupami kontenerów na różnych klastrach, sprawdza stan klastra i pilnuje żeby liczba działających podów była równa zadeklarowanej 


Podejście deklaratywne (manifesty YAML) - jest to zdefiniowanie w pliku konfiguracyjnym stanu końcowego, klaster sam analizuje różnice między stanem oczekiwanym a obecnym i uzupełnia te róniżce 


Podejście imperatywne - system instruowany jest za pomocą bezpośrednich poleceń sekwencyjnych, jest to dobre podejście do testów na żywo


Sondy monitorują mikroserwery wewnątrz klastra: 


Sonda readiness - sprawdza czy kontener jest gotowy na przyjmowanie ruchu sieciowego od użytkowników, jeśli sonda zgłosi błąd Kubernetes nie restartuje kontenera - chwilowo odłącza go od usługi sieciowej


Sonda liveness - sprawdza czy kontener żyje i czy jego proces się nie zawiesił, jeśli Kubernetes uzna kontener za martwy - zabija uszkodzony kontener i uruchamia w jego miejsce nowy 


Wnioski:


- ponieważ używam Kubenetes wbudowanego w Docker Desktop, Kubernetes nie próbuje pobierać obrazu z zewnętrznego rejstru. Klaster i Docker korzystają z tej samej pamięci, więc obraz jest już gotowy do użycia








