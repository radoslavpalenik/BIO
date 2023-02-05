# BIO - projekt
Biometrické systémy - Detekce krevního řečiště prstu z více úhlu pohledu\
Hodnotenie: 15.8/18b

## Popis
Na snímku obsahující několik různých úhlů pohled na stejný prst s NIR prosvícením, proveďte detekci krevního řečiště prstu. Na začátku rozdělte jednotlivé pohledy na prst. Na každém pohledu detekujte, extrahujte a zvýrazněte žíly.

K řešení projektu bude poskytnuta databáze snímků ze zařízení, které snímá prsty z různých úhlů pohledu. Tuto databázi by bylo vhodné jako součást práce rozšířit.

Součástí všech projektů bude obhajoba a dokumentace. Perfektní splnění projektu může vést na získání bonusových bodů v předmětu.
## Spustenie
1. krok (Spracovanie datasetu)\
`python app.py --dataInit <root dir of dataset> --output <output directory>`
2. krok (extrakcia ciev)\
`python app.py --veinsExtraction <Step 1 output> --output <output directory>`
