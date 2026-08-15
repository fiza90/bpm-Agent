import pandas as pd


class MiningService:

    def analyze_event_log(self, file):

        # =====================================================
        # 1. READ FILE
        # =====================================================

        if file.name.lower().endswith(".csv"):

            df = pd.read_csv(file)

        elif file.name.lower().endswith(".xlsx"):

            df = pd.read_excel(file)

        else:

            return {
                "status": "failed",
                "message": "Unsupported file format"
            }


        # =====================================================
        # 2. BASIC STATISTICS
        # =====================================================

        total_events = len(df)

        columns = list(df.columns)

        missing_values = (
            df.isnull()
            .sum()
            .to_dict()
        )

        duplicate_records = int(
            df.duplicated()
            .sum()
        )


        # =====================================================
        # 3. REQUIRED COLUMNS
        # =====================================================

        required_columns = [

            "Case ID",
            "Activity",
            "Timestamp",
            "Resource"

        ]

        missing_columns = [

            column

            for column in required_columns

            if column not in df.columns

        ]


        # =====================================================
        # 4. DATA QUALITY ISSUES
        # =====================================================

        issues = []


        # -----------------------------------------------------
        # Missing required columns
        # -----------------------------------------------------

        if missing_columns:

            issues.append({

                "type": "missing_column",

                "column": ", ".join(
                    missing_columns
                ),

                "count": len(
                    missing_columns
                ),

                "severity": "High",

                "message":
                f"Required column(s) missing: "
                f"{', '.join(missing_columns)}"

            })


        # =====================================================
        # 5. MISSING VALUES
        # =====================================================

        for column, count in missing_values.items():

            if count > 0:

                if column in [
                    "Case ID",
                    "Activity",
                    "Timestamp"
                ]:

                    severity = "High"

                elif column == "Resource":

                    severity = "Medium"

                else:

                    severity = "Low"


                issues.append({

                    "type": "missing_value",

                    "column": column,

                    "count": int(count),

                    "severity": severity,

                    "message":
                    f"{int(count)} missing value(s) "
                    f"found in {column}"

                })


        # =====================================================
        # 6. BLANK VALUES
        # =====================================================

        for column in df.columns:

            blank_count = (

                df[column]

                .astype(str)

                .str.strip()

                .isin([
                    "",
                    "nan",
                    "None"
                ])

                .sum()

            )


            if blank_count > 0:

                issues.append({

                    "type": "blank_value",

                    "column": column,

                    "count": int(
                        blank_count
                    ),

                    "severity":
                    "High"
                    if column in [
                        "Case ID",
                        "Activity",
                        "Timestamp"
                    ]
                    else "Medium",

                    "message":
                    f"{int(blank_count)} blank "
                    f"value(s) found in {column}"

                })


        # =====================================================
        # 7. CASE STATISTICS
        # =====================================================

        if "Case ID" in df.columns:

            total_cases = int(
                df["Case ID"]
                .nunique()
            )

        else:

            total_cases = 0


        # =====================================================
        # 8. ACTIVITY STATISTICS
        # =====================================================

        if "Activity" in df.columns:

            unique_activities = int(
                df["Activity"]
                .nunique()
            )

            activity_frequency = (

                df["Activity"]

                .value_counts()

                .to_dict()

            )

        else:

            unique_activities = 0

            activity_frequency = {}


        # =====================================================
        # 9. RESOURCE STATISTICS
        # =====================================================

        if "Resource" in df.columns:

            unique_resources = int(
                df["Resource"]
                .nunique()
            )

            resource_frequency = (

                df["Resource"]

                .value_counts()

                .to_dict()

            )

        else:

            unique_resources = 0

            resource_frequency = {}


        # =====================================================
        # 10. TIMESTAMP VALIDATION
        # =====================================================

        start_date = None

        end_date = None

        invalid_timestamp_count = 0


        if "Timestamp" in df.columns:

            df["Timestamp"] = pd.to_datetime(

                df["Timestamp"],

                errors="coerce"

            )


            invalid_timestamp_count = int(

                df["Timestamp"]
                .isnull()
                .sum()

            )


            if invalid_timestamp_count > 0:

                issues.append({

                    "type":
                    "invalid_timestamp",

                    "column":
                    "Timestamp",

                    "count":
                    invalid_timestamp_count,

                    "severity":
                    "High",

                    "message":
                    f"{invalid_timestamp_count} "
                    f"invalid timestamp(s) found"

                })


            valid_timestamps = df[
                "Timestamp"
            ].dropna()


            if not valid_timestamps.empty:

                start_date = str(
                    valid_timestamps.min()
                )

                end_date = str(
                    valid_timestamps.max()
                )


        # =====================================================
        # 11. DUPLICATE RECORDS
        # =====================================================

        if duplicate_records > 0:

            issues.append({

                "type":
                "duplicate",

                "column":
                "All columns",

                "count":
                duplicate_records,

                "severity":
                "Medium",

                "message":
                f"{duplicate_records} "
                f"duplicate record(s) found"

            })


        # =====================================================
        # 12. DUPLICATE EVENTS
        # =====================================================

        if all(
            column in df.columns
            for column in [
                "Case ID",
                "Activity",
                "Timestamp"
            ]
        ):

            duplicate_events = int(

                df.duplicated(

                    subset=[
                        "Case ID",
                        "Activity",
                        "Timestamp"
                    ]

                ).sum()

            )


            if duplicate_events > 0:

                issues.append({

                    "type":
                    "duplicate_event",

                    "column":
                    "Case ID + Activity + Timestamp",

                    "count":
                    duplicate_events,

                    "severity":
                    "Medium",

                    "message":
                    f"{duplicate_events} "
                    f"duplicate event(s) found"
                })

        else:

            duplicate_events = 0


        # =====================================================
        # 13. OUT-OF-ORDER EVENTS
        # =====================================================

        out_of_order_cases = 0

        if all(
            column in df.columns
            for column in [
                "Case ID",
                "Timestamp"
            ]
        ):

            valid_df = df.dropna(

                subset=[
                    "Case ID",
                    "Timestamp"
                ]

            ).copy()


            if not valid_df.empty:

                valid_df = valid_df.sort_values(
                    [
                        "Case ID",
                        "Timestamp"
                    ]
                )


                original_order = df[
                    [
                        "Case ID",
                        "Timestamp"
                    ]
                ].dropna()


                for case_id, group in original_order.groupby(
                    "Case ID"
                ):

                    timestamps = group[
                        "Timestamp"
                    ].tolist()


                    if timestamps != sorted(
                        timestamps
                    ):

                        out_of_order_cases += 1


        if out_of_order_cases > 0:

            issues.append({

                "type":
                "out_of_order",

                "column":
                "Timestamp",

                "count":
                out_of_order_cases,

                "severity":
                "Medium",

                "message":
                f"{out_of_order_cases} case(s) "
                f"contain events that are not "
                f"in chronological order"

            })


        # =====================================================
        # 14. CASES WITH ONLY ONE EVENT
        # =====================================================

        single_event_cases = 0


        if "Case ID" in df.columns:

            case_event_counts = (

                df.groupby(
                    "Case ID"
                )
                .size()

            )


            single_event_cases = int(

                (
                    case_event_counts == 1
                )
                .sum()

            )


            if single_event_cases > 0:

                issues.append({

                    "type":
                    "single_event_case",

                    "column":
                    "Case ID",

                    "count":
                    single_event_cases,

                    "severity":
                    "Low",

                    "message":
                    f"{single_event_cases} case(s) "
                    f"contain only one event"

                })


        # =====================================================
        # 15. PROCESS DURATION CHECK
        # =====================================================

        average_case_duration_days = None

        if all(
            column in df.columns
            for column in [
                "Case ID",
                "Timestamp"
            ]
        ):

            valid_df = df.dropna(

                subset=[
                    "Case ID",
                    "Timestamp"
                ]

            )


            if not valid_df.empty:

                case_durations = (

                    valid_df
                    .groupby("Case ID")[
                        "Timestamp"
                    ]
                    .agg(
                        lambda x:
                        (
                            x.max() - x.min()
                        ).total_seconds()
                        / 86400
                    )

                )


                if not case_durations.empty:

                    average_case_duration_days = round(

                        case_durations.mean(),

                        2

                    )


        # =====================================================
        # 16. DATA QUALITY SCORE
        # =====================================================

        high_issues = sum(

            1

            for issue in issues

            if issue["severity"] == "High"

        )


        medium_issues = sum(

            1

            for issue in issues

            if issue["severity"] == "Medium"

        )


        low_issues = sum(

            1

            for issue in issues

            if issue["severity"] == "Low"

        )


        if total_events == 0:

            data_quality_score = 0

        else:

            issue_penalty = (

                (high_issues * 10)

                + (medium_issues * 5)

                + (low_issues * 2)

            )


            data_quality_score = max(

                0,

                min(
                    100,
                    100 - issue_penalty
                )

            )


        # =====================================================
        # 17. DATA QUALITY STATUS
        # =====================================================

        if high_issues > 0:

            data_quality = "Poor"

            readiness = (
                "Data Cleaning Required"
            )

        elif medium_issues > 0:

            data_quality = "Needs Review"

            readiness = (
                "Review Before Process Mining"
            )

        elif low_issues > 0:

            data_quality = "Good"

            readiness = (
                "Ready for Process Mining"
            )

        else:

            data_quality = "Excellent"

            readiness = (
                "Ready for Process Mining"
            )


        # =====================================================
        # 18. RECOMMENDATIONS
        # =====================================================

        recommendations = []


        if high_issues > 0:

            recommendations.append(

                "Correct all high-severity "
                "data quality issues before "
                "process discovery."

            )


        if missing_values.get("Timestamp", 0) > 0:

            recommendations.append(

                "Complete missing timestamps "
                "to enable accurate cycle-time "
                "and bottleneck analysis."

            )


        if invalid_timestamp_count > 0:

            recommendations.append(

                "Correct invalid timestamps "
                "before running process mining."

            )


        if duplicate_records > 0:

            recommendations.append(

                "Investigate and remove "
                "duplicate records where appropriate."

            )


        if out_of_order_cases > 0:

            recommendations.append(

                "Review event ordering within "
                "affected cases."

            )


        if single_event_cases > 0:

            recommendations.append(

                "Review single-event cases because "
                "they may represent incomplete "
                "process instances."

            )


        if not recommendations:

            recommendations.append(

                "No major data quality issues "
                "were detected. The event log "
                "is suitable for process mining."

            )


        # =====================================================
        # 19. FINAL RESPONSE
        # =====================================================

        return {

            "status":
            "completed",


            "data_quality":
            data_quality,


            "data_quality_score":
            data_quality_score,


            "readiness":
            readiness,


            "summary": {

                "total_events":
                total_events,

                "total_cases":
                total_cases,

                "unique_activities":
                unique_activities,

                "unique_resources":
                unique_resources,

                "start_date":
                start_date,

                "end_date":
                end_date,

                "average_case_duration_days":
                average_case_duration_days

            },


            "activity_frequency":
            activity_frequency,


            "resource_frequency":
            resource_frequency,


            "missing_values":
            missing_values,


            "duplicate_records":
            duplicate_records,


            "duplicate_events":
            duplicate_events,


            "missing_columns":
            missing_columns,


            "invalid_timestamps":
            invalid_timestamp_count,


            "out_of_order_cases":
            out_of_order_cases,


            "single_event_cases":
            single_event_cases,


            "issues":
            issues,


            "recommendations":
            recommendations

        }