terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Service Account for ADK Blog Writer Agent Fleet
resource "google_service_account" "blog_writer_sa" {
  account_id   = "blog-writer-agent-sa"
  display_name = "Automated Blog Writer ADK 2.0 Agent Fleet Service Account"
}

# 2. GCS Bucket for Published Articles & Assets
resource "google_storage_bucket" "articles_bucket" {
  name                        = "blog-writer-articles-${var.project_id}"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# 3. GCS Bucket for Audit Logs & Judge Records
resource "google_storage_bucket" "audit_bucket" {
  name                        = "blog-writer-audit-${var.project_id}"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true
}

# 4. BigQuery Analytical Dataset for Persistent Audit Logs
resource "google_bigquery_dataset" "audit_dataset" {
  dataset_id                  = "blog_system_audit"
  friendly_name               = "Blog Writer Multi-Agent Audit Dataset"
  description                 = "Persistent audit trail for Judge decisions, rubric scores, and agent hand-offs"
  location                    = var.region
  default_table_expiration_ms = 315360000000 # 10 Years
}

# 5. BigQuery Judge Decision Table Schema
resource "google_bigquery_table" "judge_decisions_table" {
  dataset_id = google_bigquery_dataset.audit_dataset.dataset_id
  table_id   = "judge_decisions_v1"

  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }

  schema = <<EOF
[
  {"name": "judgment_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "task_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "session_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "domain", "type": "STRING", "mode": "REQUIRED"},
  {"name": "writer_agent_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "iteration_number", "type": "INTEGER", "mode": "REQUIRED"},
  {"name": "decision", "type": "STRING", "mode": "REQUIRED"},
  {"name": "article_title", "type": "STRING", "mode": "REQUIRED"},
  {"name": "hero_image_url", "type": "STRING", "mode": "REQUIRED"},
  {"name": "rubric_coherence", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "rubric_alignment", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "rubric_fluency", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "rubric_image_relevance", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "rubric_image_quality", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "rubric_composite", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "critique", "type": "STRING", "mode": "NULLABLE"},
  {"name": "detailed_considerations", "type": "STRING", "mode": "NULLABLE"},
  {"name": "required_revisions", "type": "STRING", "mode": "REPEATED"}
]
EOF
}

# 6. IAM Role Bindings for Service Account
resource "google_project_iam_member" "sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.blog_writer_sa.email}"
}

resource "google_project_iam_member" "sa_bq_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.blog_writer_sa.email}"
}

resource "google_project_iam_member" "sa_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.blog_writer_sa.email}"
}
