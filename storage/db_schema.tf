terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "~> 1.21"
    }
  }
}

variable "db_host" {
  type = string
}

variable "db_port" {
  type    = number
  default = 5432
}

variable "db_name" {
  type = string
}

variable "db_user" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

provider "postgresql" {
  host     = var.db_host
  port     = var.db_port
  database = var.db_name
  username = var.db_user
  password = var.db_password
  sslmode  = "require"
}

resource "postgresql_table" "stocks" {
  name   = "stocks"
  schema = "public"

  column {
    name     = "symbol"
    type     = "text"
    nullable = false
  }

  column {
    name     = "last_updated"
    type     = "timestamp"
    default  = "CURRENT_TIMESTAMP"
    nullable = false
  }

  primary_key {
    name    = "stocks_pkey"
    columns = ["symbol"]
  }
}

resource "postgresql_table" "daily_prices" {
  name   = "daily_prices"
  schema = "public"

  column {
    name     = "id"
    type     = "serial"
    nullable = false
  }

  column {
    name     = "symbol"
    type     = "text"
    nullable = false
  }

  column {
    name     = "date"
    type     = "date"
    nullable = false
  }

  column {
    name     = "open"
    type     = "real"
    nullable = false
  }

  column {
    name     = "high"
    type     = "real"
    nullable = false
  }

  column {
    name     = "low"
    type     = "real"
    nullable = false
  }

  column {
    name     = "close"
    type     = "real"
    nullable = false
  }

  column {
    name     = "volume"
    type     = "bigint"
    nullable = false
  }

  primary_key {
    name    = "daily_prices_pkey"
    columns = ["id"]
  }
}

resource "postgresql_index" "daily_prices_symbol_date_unique" {
  name   = "daily_prices_symbol_date_key"
  schema = "public"
  table  = postgresql_table.daily_prices.name
  unique = true
  columns = [
    "symbol",
    "date",
  ]
}

resource "postgresql_index" "daily_prices_symbol_date_idx" {
  name   = "idx_daily_prices_symbol_date"
  schema = "public"
  table  = postgresql_table.daily_prices.name
  columns = [
    "symbol",
    "date",
  ]
}
