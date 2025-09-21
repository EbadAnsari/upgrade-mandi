Example for the Id include `Ayodhya Nagar` with date `02-08-2025`

Invoice Number Formula:

```javascript
INV-<YYYY><MM><DD>-UM-<LOCATION-3-LETTERS>-<INVOICE-VERSION>
```

Example

```
INV-20250802-UM-AYD-1
```

Database Invoice Primary Key Formula: `INV-<YYYYMMDD>-UM-<LOCATION-3-LETTERS>-<Invoice-Version>`

GRN Number Formula:

```javascript
GRN_IM#<INVOICE-NUMBER>#<SUPPLIER-ID>
```

Example

```
GRN_IM#11082025UMAN1#74227878
```

| Location      | Code  |
| ------------- | ----- |
| Ayodhya Nagar | (AYD) |
| Byramji       | (BRJ) |
| Dharampeth    | (DRM) |
| Mahal         | (MHL) |
| Manish Nagar  | (MNS) |
| Nandanvan     | (NDV) |
| Sai Mandi     | (SIM) |

TODO:

-   optimize the dataset so that it can read multiple rows of records
-   error handle for while entering the wrong file
-   embeded `rich` text
-   preprocess data before loading the dataset

New-Item -ItemType SymbolicLink -Path "data" -Target "..\upgrade_mandi\data\"
