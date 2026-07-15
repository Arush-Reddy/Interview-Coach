def build_report(evaluations):
    """Build a final report from the answers evaluated in this interview."""
    records = list(evaluations.values())
    if not records:
        return None

    average_score = round(sum(record["feedback"]["score"] for record in records) / len(records), 1)
    average_communication = round(
        sum(record["communication"]["communication_score"] for record in records) / len(records), 1
    )
    total_fillers = sum(record["communication"]["total_fillers"] for record in records)
    best_record = max(records, key=lambda record: record["feedback"]["score"])
    improvement_record = min(records, key=lambda record: record["feedback"]["score"])

    recommendations = []
    if average_score < 7:
        recommendations.append("Use the STAR method to give more complete examples.")
    if average_communication < 7:
        recommendations.append("Slow down and reduce filler words before moving to your next point.")
    if total_fillers > len(records) * 2:
        recommendations.append("Pause briefly instead of using filler words such as 'um' or 'like'.")
    if not recommendations:
        recommendations.append("Keep practising with more specific examples from your projects and experiences.")

    return {
        "answers_evaluated": len(records),
        "average_score": average_score,
        "average_communication": average_communication,
        "total_fillers": total_fillers,
        "best_question": best_record["question"],
        "improvement_question": improvement_record["question"],
        "recommendations": recommendations,
    }


def report_as_markdown(report):
    recommendations = "\n".join(f"- {item}" for item in report["recommendations"])
    return f"""# AI Interview Coach Report

## Results
- Answers evaluated: {report["answers_evaluated"]}
- Average answer score: {report["average_score"]}/10
- Average communication score: {report["average_communication"]}/10
- Total filler words: {report["total_fillers"]}

## Best Answer
{report["best_question"]}

## Main Improvement Area
{report["improvement_question"]}

## Recommendations
{recommendations}
"""
