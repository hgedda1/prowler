from prowler.lib.check.models import Check, Check_Report_AWS
from prowler.providers.aws.services.redshift.redshift_client import redshift_client


class redshift_cluster_kms_enabled(Check):
    def execute(self):
        findings = []

        # Iterate over all Redshift clusters
        for cluster in redshift_client.clusters:
            report = Check_Report_AWS(self.metadata())
            report.region = cluster.region
            report.resource_id = cluster.id
            report.resource_arn = cluster.arn
            report.resource_tags = cluster.tags

            # Check if the cluster is encrypted with KMS
            if cluster.encrypted and cluster.kms_key_id:
                report.status = "PASS"
                report.status_extended = f"Redshift cluster {cluster.id} is encrypted with KMS key {cluster.kms_key_id}."
            else:
                report.status = "FAIL"
                report.status_extended = (
                    f"Redshift cluster {cluster.id} is not encrypted with KMS."
                )

            # Append the report to the findings list
            findings.append(report)

        return findings
