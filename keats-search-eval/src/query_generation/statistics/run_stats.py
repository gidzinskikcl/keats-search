import pandas as pd
from scipy.stats import chisquare


def main():
    # Load the dataset
    # file_path = "keats-search-eval/data/queries/validated/keats-search_queries_24-06-2025.csv"

    # file_path = "keats-search-eval/data/queries/validated/keats-search_queries_with_content_24-06-2025.csv" # this one was used originally
    file_path = "keats-search-eval/data/queries/validated/keats-search_queries_with_content_21-07-2025.csv"

    df = pd.read_csv(file_path, sep=",")

    # Step 1: Count excluded queries
    excluded_pre_annotation = df[df["label"] == "empty"]
    excluded_annotation = df[
        df["label"].isin(["invalid", "administrative", "extrapolated"])
    ]

    # Step 2: Assess total and proportions
    total_queries = len(df)
    valid_queries = df[df["label"] == "valid"]
    n_valid = len(valid_queries)
    excluded_pre_annotation = df[df["label"] == "empty"]
    excluded_invalid = df[df["label"].isin(["invalid", "extrapolated"])]
    excluded_administrative = df[df["label"] == "administrative"]

    n_excluded_empty = len(excluded_pre_annotation)
    n_excluded_invalid = len(excluded_invalid)
    n_excluded_admin = len(excluded_administrative)

    n_excluded_total = n_excluded_empty + n_excluded_invalid + n_excluded_admin
    n_remaining = total_queries - n_excluded_total

    # Create table
    data = [
        ["Total queries", total_queries, f"{100:.2f}%"],
        ["Empty", n_excluded_empty, f"{n_excluded_empty / total_queries:.2%}"],
        ["Invalid", n_excluded_invalid, f"{n_excluded_invalid / total_queries:.2%}"],
        ["Administrative", n_excluded_admin, f"{n_excluded_admin / total_queries:.2%}"],
        ["Total excluded", n_excluded_total, f"{n_excluded_total / total_queries:.2%}"],
        ["Remaining", n_remaining, f"{n_remaining / total_queries:.2%}"],
    ]

    df_table = pd.DataFrame(data, columns=["Category", "Count", "Percentage"])

    print(df_table.to_string(index=False))

    # Export LaTeX
    latex_table = df_table.to_latex(index=False, escape=False)
    output_tex = (
        "keats-search-eval/data/queries/results/llm_query_generation_summary.tex"
    )
    with open(output_tex, "w") as f:
        f.write(latex_table)

    print(f"\n✅ Saved summary to {output_tex}")

    # Console print summary
    print("\n==== Query Exclusion Statistics ====")
    print(f"Total queries: {total_queries} ({100:.2f}%)")
    print(
        f"Excluded as empty/image-only: {n_excluded_empty} ({n_excluded_empty / total_queries:.2%})"
    )
    print(
        f"Excluded as invalid (including extrapolated): {n_excluded_invalid} ({n_excluded_invalid / total_queries:.2%})"
    )
    print(
        f"Excluded as administrative: {n_excluded_admin} ({n_excluded_admin / total_queries:.2%})"
    )
    print(
        f"Total excluded: {n_excluded_total} ({n_excluded_total / total_queries:.2%})"
    )
    print(
        f"Remaining after exclusion: {n_remaining} ({n_remaining / total_queries:.2%})"
    )

    # Exclusions by course
    print("\n-- Excluded Queries by Course --")
    for course in df["course_name"].unique():
        total = len(df[df["course_name"] == course])
        empty = len(df[(df["course_name"] == course) & (df["label"] == "empty")])
        invalid = len(df[(df["course_name"] == course) & (df["label"] == "invalid")])
        admin = len(
            df[(df["course_name"] == course) & (df["label"] == "administrative")]
        )
        excluded = empty + invalid + admin
        print(f"{course}:")
        print(f"  Total: {total}")
        print(f"  Empty/image-only: {empty}")
        print(f"  Invalid: {invalid}")
        print(f"  Administrative: {admin}")
        print(f"  Total excluded: {excluded} ({excluded / total:.2%})")

    # # Step 3: Distribution across courses
    # print("\n==== Query Distribution by Course ====")

    # # All queries
    # print("\n-- All Queries --")
    # all_course_counts = df["course_name"].value_counts()
    # all_course_props = df["course_name"].value_counts(normalize=True)
    # for course in all_course_counts.index:
    #     print(
    #         f"{course}: {all_course_counts[course]} queries ({all_course_props[course]:.2%})"
    #     )

    # # Valid queries only
    # print("\n-- Valid Queries Only --")
    # valid_course_counts = valid_queries["course_name"].value_counts()
    # valid_course_props = valid_queries["course_name"].value_counts(normalize=True)
    # for course in valid_course_counts.index:
    #     print(
    #         f"{course}: {valid_course_counts[course]} valid queries ({valid_course_props[course]:.2%})"
    #     )

    # # Step 4: Distribution across lectures within each course
    # print("\n==== Query Distribution by Lecture (per Course) ====")
    # grouped = (
    #     df.groupby(["course_name", "lecture_title"])
    #     .size()
    #     .reset_index(name="query_count")
    # )
    # for course in df["course_name"].unique():
    #     print(f"\nCourse: {course}")
    #     course_lectures = grouped[grouped["course_name"] == course]
    #     for _, row in course_lectures.iterrows():
    #         print(f"  Lecture: {row['lecture_title']} - {row['query_count']} queries")

    # # Step 5: Source breakdown (SRT vs PDF)
    # print("\n==== Query Source Statistics ====")
    # from_srt = df[df["doc_id"].str.endswith("_srt")]
    # from_pdf = df[df["doc_id"].str.endswith("_pdf")]
    # print(f"Queries from SRT: {len(from_srt)} ({len(from_srt) / total_queries:.2%})")
    # print(f"Queries from PDF: {len(from_pdf)} ({len(from_pdf) / total_queries:.2%})")

    # # Step 6: Query distribution outliers per lecture
    # print("\n==== Outlier Lectures Based on Query Counts ====")
    # lecture_totals = (
    #     valid_queries.groupby(["course_name", "lecture_title"])
    #     .size()
    #     .reset_index(name="query_count")
    # )
    # for course in lecture_totals["course_name"].unique():
    #     course_lectures = lecture_totals[lecture_totals["course_name"] == course]
    #     q1 = course_lectures["query_count"].quantile(0.25)
    #     q3 = course_lectures["query_count"].quantile(0.75)
    #     iqr = q3 - q1
    #     low_thresh = q1 - 1.5 * iqr
    #     high_thresh = q3 + 1.5 * iqr
    #     low_outliers = course_lectures[course_lectures["query_count"] < low_thresh]
    #     high_outliers = course_lectures[course_lectures["query_count"] > high_thresh]
    #     print(f"\nCourse: {course}")
    #     print(f"  Lectures with very few queries: {len(low_outliers)}")
    #     print(f"  Lectures with very many queries: {len(high_outliers)}")

    # # Step 7: Segments with multiple queries
    # print("\n==== Segments With More Than One Valid Query ====")
    # segment_counts = valid_queries.groupby(
    #     ["course_name", "lecture_title", "doc_id"]
    # ).size()
    # segments_multiple = segment_counts[segment_counts > 1]
    # print(f"Segments with >1 valid query: {len(segments_multiple)}")
    # print(f"Percentage: {len(segments_multiple) / segment_counts.shape[0]:.2%}")

    # # Extract and show questions per such segment
    # print("\n-- Segments and Their Valid Questions --")
    # multi_query_segments = segments_multiple.reset_index()[
    #     ["course_name", "lecture_title", "doc_id"]
    # ]

    # for _, row in multi_query_segments.iterrows():
    #     course, lecture, doc = row["course_name"], row["lecture_title"], row["doc_id"]
    #     queries = valid_queries[
    #         (valid_queries["course_name"] == course)
    #         & (valid_queries["lecture_title"] == lecture)
    #         & (valid_queries["doc_id"] == doc)
    #     ][["question"]]

    #     print(
    #         f"\nCourse: {course} | Lecture: {lecture} | Doc: {doc} | Queries: {len(queries)}"
    #     )
    #     for i, q in enumerate(queries["question"], 1):
    #         print(f"  {i}. {q}")

    # # Step 8: Duplicate valid queries (excluding 'empty')
    # print("\n==== Duplicate Valid Queries (Excluding Empty) ====")
    # non_empty_valids = df[(df["label"] == "valid") & (df["question"].notna())]
    # duplicate_questions = non_empty_valids.duplicated(subset="question", keep=False)
    # num_duplicates = duplicate_questions.sum()
    # print(
    #     f"Duplicate valid questions: {num_duplicates} ({num_duplicates / len(non_empty_valids):.2%})"
    # )

    # # Optional: show top repeated questions (optional detail)
    # dup_qs = non_empty_valids[duplicate_questions]
    # top_duplicates = dup_qs["question"].value_counts().head(5)
    # if not top_duplicates.empty:
    #     print("\nTop duplicate valid questions:")
    #     print(top_duplicates)

    # Step 9: Difficulty level distribution
    print("\n==== Difficulty Level Distribution (Valid Queries Only) ====")
    difficulty_counts = valid_queries["difficulty"].value_counts()
    difficulty_props = valid_queries["difficulty"].value_counts(normalize=True)
    for level in difficulty_counts.index:
        print(f"{level}: {difficulty_counts[level]} ({difficulty_props[level]:.2%})")

    # print("\n==== Chi-Square Test for Course Query Distribution ====")
    # course_query_counts = valid_queries["course_name"].value_counts()
    # expected = [course_query_counts.mean()] * len(course_query_counts)
    # chi2, p = chisquare(course_query_counts, f_exp=expected)
    # print(f"Chi-square statistic: {chi2:.2f}, p-value: {p:.4f}")
    # if p < 0.05:
    #     print("⚠️ Significant disproportions between courses.")
    # else:
    #     print("✅ No significant disproportions between courses.")

    # print("\n==== Chi-Square Test for Difficulty Distribution ====")
    # difficulty_counts = valid_queries["difficulty"].value_counts()
    # expected = [difficulty_counts.mean()] * len(difficulty_counts)
    # chi2, p = chisquare(difficulty_counts, f_exp=expected)
    # print(f"Chi-square statistic: {chi2:.2f}, p-value: {p:.4f}")
    # if p < 0.05:
    #     print("⚠️ Significant imbalance in difficulty levels.")
    # else:
    #     print("✅ Difficulty levels are relatively balanced.")

    # print("\n==== Source Distribution Balance Check ====")
    # source_counts = (
    #     valid_queries["doc_id"]
    #     .apply(lambda x: "SRT" if x.endswith(".srt") else "PDF")
    #     .value_counts()
    # )
    # expected = [source_counts.mean()] * len(source_counts)
    # chi2, p = chisquare(source_counts, f_exp=expected)
    # print(f"Chi-square statistic: {chi2:.2f}, p-value: {p:.4f}")
    # if p < 0.05:
    #     print("⚠️ Imbalance between PDF and SRT sources.")
    # else:
    #     print("✅ Sources are relatively balanced.")

    # duplicate_ratio = num_duplicates / len(valid_queries)
    # print(f"\n==== Duplicate Coverage ====")
    # print(f"Duplicate valid queries (global): {duplicate_ratio:.2%}")
    # if duplicate_ratio > 0.1:
    #     print("⚠️ High duplication may bias evaluation.")
    # else:
    #     print("✅ Low duplication risk.")


if __name__ == "__main__":
    main()
