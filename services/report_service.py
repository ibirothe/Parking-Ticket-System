import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db):
        self.db = db
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, report_type):
        report_type = report_type.lower()
        if report_type == "occupancy":
            self._report_occupancy()
        elif report_type == "clusters":
            self._report_clusters()
        else:
            logger.warning("Unknown report type: %s", report_type)

    def _report_occupancy(self):
        query = "SELECT slot_number, occupied FROM slots ORDER BY slot_number"
        df = pd.read_sql_query(query, self.db.connection)
        occupied = df["occupied"].sum()
        available = len(df) - occupied

        plt.figure()
        plt.pie([occupied, available], labels=["Occupied", "Available"], autopct="%1.1f%%")
        plt.title("Current Parking Occupancy")
        output_path = os.path.join(self.output_dir, f"occupancy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(output_path)
        plt.close()
        logger.info("Occupancy report saved to %s", output_path)

    def _report_clusters(self):
        query = "SELECT slot_number, occupied FROM slots ORDER BY slot_number"
        df = pd.read_sql_query(query, self.db.connection)

        # Car cluster detection
        clusters = []
        current_cluster_size = 0
        for _, row in df.iterrows():
            if row["occupied"] == 1:
                current_cluster_size += 1
            else:
                if current_cluster_size > 0:
                    clusters.append(current_cluster_size)
                    current_cluster_size = 0
        if current_cluster_size > 0:
            clusters.append(current_cluster_size)

        if not clusters:
            logger.info("No occupied clusters found.")
            return

        # Count clusters by size
        cluster_counts = pd.Series(clusters).value_counts().sort_index()

        plt.figure()
        cluster_counts.plot(kind="bar")
        plt.title("Cluster Size Distribution")
        plt.xlabel("Cluster Size (cars)")
        plt.ylabel("Number of Clusters")
        plt.xticks(rotation=0)
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, f"clusters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(output_path)
        plt.close()
        logger.info(
            "Cluster report saved to %s. Found %d clusters, sizes: %s",
            output_path,
            len(clusters),
            clusters,
        )
