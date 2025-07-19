from enum import Enum
class ReportRoutes(Enum):
    REPORT_GENERATOR = "report.generator"
    REPORT_VIEWER    = "report.viewer"
    CHART_DESIGNER   = "chart.designer"
    def __str__(self) -> str:
        return self.value