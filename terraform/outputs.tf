output "service_account_email" {
  value       = google_service_account.blog_writer_sa.email
  description = "Email of the deployed agent fleet Service Account"
}

output "articles_bucket_name" {
  value       = google_storage_bucket.articles_bucket.name
  description = "Name of the GCS bucket for published blog posts"
}

output "audit_bucket_name" {
  value       = google_storage_bucket.audit_bucket.name
  description = "Name of the GCS bucket for persistent JSON audit logs"
}

output "bigquery_audit_table" {
  value       = "${google_bigquery_dataset.audit_dataset.dataset_id}.${google_bigquery_table.judge_decisions_table.table_id}"
  description = "BigQuery dataset and table for Judge decision audit logs"
}
