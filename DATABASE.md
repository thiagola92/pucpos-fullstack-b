# Banco de Dados
```mermaid
classDiagram
  Accounts -- PropertyOwners
  Properties -- PropertyOwners

  class Accounts {
    id
    email
    phone
    password
  }

  class Properties {
    id
    address_id
    price
    plan_id
    type_id
    photo
  }

  class PropertyOwners {
    id
    account_id
    property_id
  }
```

---

```mermaid
classDiagram
  Properties -- Addresses
  Properties -- Plans
  Properties -- Types

  class Addresses {
    id
    country
    state
    city
    street
    house_number
    extra
  }

  class Plans {
    id
    action
  }

  class Types {
    id
    name
  }

  class Properties {
    id
    address_id
    price
    plan_id
    type_id
    photo
  }
```
