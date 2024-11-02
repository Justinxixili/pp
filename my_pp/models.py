
from django.db import models


class Patent(models.Model):
    patent_id = models.CharField(max_length=100, unique=True)  # publication_number
    title = models.TextField(null=True, blank=True)  # 设置为可空
    abstract = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assignee = models.CharField(max_length=255, null=True, blank=True)
    inventors = models.JSONField(null=True, blank=True)
    priority_date = models.DateField(null=True, blank=True)
    application_date = models.DateField(null=True, blank=True)
    grant_date = models.DateField(null=True, blank=True)
    claims = models.JSONField()
    jurisdictions = models.CharField(max_length=50, null=True, blank=True)
    classifications = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.patent_id}: {self.title}"


class Company(models.Model):
    name = models.CharField(max_length=200)
    products = models.JSONField()

    def __str__(self):
        return self.name


class InfringementReport(models.Model):
    patent = models.ForeignKey(Patent, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    analysis_date = models.DateTimeField(auto_now_add=True)
    top_infringing_products = models.JSONField()
    overall_risk_assessment = models.TextField()

    class Meta:
        ordering = ['-analysis_date']