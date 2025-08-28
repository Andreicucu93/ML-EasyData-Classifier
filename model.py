# --- Minimal ML for Category + Subcategory from product Name ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score


def run_model_1target(path, feature_column, target_column_1, new_products: list):
    DATA_PATH = path
    SHEET_NAME = None
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME or 0)
    xls = pd.ExcelFile(DATA_PATH)
    sheet = SHEET_NAME or xls.sheet_names[0]

    df = df.copy()
    df[feature_column] = df[feature_column].astype(str)

    # A) --- Train Category model (feature_column -> target_column_1)
    #    We drop rows where attribute is missing, because we need examples with labels to learn from.
    tg1_df = df.dropna(subset=[target_column_1]).copy()

    #    Split the known labeled data into train/test to quickly check model quality.
    y_all = tg1_df[target_column_1].astype(str)
    counts = y_all.value_counts()
    use_stratify = counts.min() >= 2  # only stratify if safe

    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        tg1_df[feature_column],
        y_all,
        test_size=0.2,
        random_state=42,
        stratify=y_all if use_stratify else None
    )

    #    Build a tiny pipeline: TF-IDF (turn words into numbers) + Logistic Regression (classifier).
    target_1 = make_pipeline(
        TfidfVectorizer(
            ngram_range=(1, 2),   # use single words and 2-word phrases (bigrams)
            lowercase=True,
            min_df=2              # ignore words that appear only once (reduces noise)
        ),
        LogisticRegression(
            max_iter=1000,        # allow enough iterations to converge
            class_weight="balanced"  # help with rare categories
        )
    )

    #    Train on training data.
    target_1.fit(Xc_train, yc_train)

    #    Quick sanity check: how well does it perform on held-out test data?
    yc_pred = target_1.predict(Xc_test)
    print("First attribute accuracy:", round(accuracy_score(yc_test, yc_pred), 4))
    print(classification_report(yc_test, yc_pred))


    # 7) --- Predict for ANY list of new product names (this is what you asked for) ---
    #    Edit this list with whatever products you want to classify.


    #    Make predictions for each product in the list using both models.
    results = []
    for name in new_products:
        pred_tg1 = target_1.predict([name])[0]  # Category prediction (string)
        results.append({
            "Item": name,
            "Target": pred_tg1
        })

    # 8) Show predictions as a simple table
    output = pd.DataFrame(results)
    return output

def run_model_2target(path, feature_column, target_column_1, target_column_2, new_products):
    DATA_PATH = path
    SHEET_NAME = None
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME or 0)
    xls = pd.ExcelFile(DATA_PATH)
    sheet = SHEET_NAME or xls.sheet_names[0]
    # will rename to variable
    #    (We train on rows where the target exists; later we can predict for any new list)
    df = df.copy()
    df[feature_column] = df[feature_column].astype(str)

    # A) --- Train Category model (feature_column -> target_column_1)
    #    We drop rows where attribute is missing, because we need examples with labels to learn from.
    cat_df = df.dropna(subset=[target_column_1]).copy()

    #    Split the known labeled data into train/test to quickly check model quality.
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        cat_df[feature_column],                     # input text (product name)
        cat_df[target_column_1].astype(str),     # target label (Category)
        test_size=0.2,                      # 20% of data held out for testing
        random_state=42,                    # makes results reproducible
        stratify=cat_df[target_column_1].astype(str)  # keep class balance in split
    )

    #    Build a tiny pipeline: TF-IDF (turn words into numbers) + Logistic Regression (classifier).
    cat_model = make_pipeline(
        TfidfVectorizer(
            ngram_range=(1, 2),   # use single words and 2-word phrases (bigrams)
            lowercase=True,
            min_df=2              # ignore words that appear only once (reduces noise)
        ),
        LogisticRegression(
            max_iter=1000,        # allow enough iterations to converge
            class_weight="balanced"  # help with rare categories
        )
    )

    #    Train on training data.
    cat_model.fit(Xc_train, yc_train)

    #    Quick sanity check: how well does it perform on held-out test data?
    yc_pred = cat_model.predict(Xc_test)
    print("First attribute accuracy:", round(accuracy_score(yc_test, yc_pred), 4))
    print(classification_report(yc_test, yc_pred))


    # B) --- Same recipe, trained separately for target_column_2 -- other variables
    sub_df = df.dropna(subset=[target_column_2]).copy()

    Xs_train, Xs_test, ys_train, ys_test = train_test_split(
        sub_df[feature_column],
        sub_df[target_column_2].astype(str),
        test_size=0.2,
        random_state=42,
        stratify=sub_df[target_column_2].astype(str)
    )

    sub_model = make_pipeline(
        TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            min_df=2
        ),
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )

    sub_model.fit(Xs_train, ys_train)

    ys_pred = sub_model.predict(Xs_test)
    print("Second attribute accuracy:", round(accuracy_score(ys_test, ys_pred), 4))
    print(classification_report(ys_test, ys_pred))

    # 7) --- Predict for ANY list of new product names (this is what you asked for) ---
    #    Edit this list with whatever products you want to classify.

    #    Make predictions for each product in the list using both models.
    results = []
    for name in new_products:
        pred_cat = cat_model.predict([name])[0]  # Category prediction (string)
        pred_sub = sub_model.predict([name])[0]  # Subcategory prediction (string)
        results.append({
            "Name": name,
            "PredictedCategory": pred_cat,
            "PredictedSubcategory": pred_sub
        })

    # 8) Show predictions as a simple table
    pd.DataFrame(results)
