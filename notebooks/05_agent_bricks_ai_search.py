# Databricks notebook source
# MAGIC %md
# MAGIC # 05. Agent Bricks AI Search 용어집 구성
# MAGIC
# MAGIC `glossary.csv`를 Delta 테이블로 만들고 Triggered Delta Sync Index를 생성합니다.

# COMMAND ----------

# MAGIC %pip install -q --upgrade databricks-ai-search
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

dbutils.widgets.text("catalog", "issu_dip_wksp", "Catalog")
dbutils.widgets.text("landing_schema", "gasentec_landing", "Landing schema")
dbutils.widgets.text("analytics_schema", "gasentec_hands_on", "Analytics schema")
dbutils.widgets.text("endpoint_name", "gasentec-ai-search-endpoint", "AI Search endpoint")
dbutils.widgets.text("embedding_model", "databricks-qwen3-embedding-0-6b", "Embedding model")

catalog = dbutils.widgets.get("catalog")
landing_schema = dbutils.widgets.get("landing_schema")
analytics_schema = dbutils.widgets.get("analytics_schema")
endpoint_name = dbutils.widgets.get("endpoint_name")
embedding_model = dbutils.widgets.get("embedding_model")

source_table = f"{catalog}.{analytics_schema}.gasentec_lng_glossary"
index_name = f"{catalog}.{analytics_schema}.gasentec_lng_glossary_index"
glossary_path = f"/Volumes/{catalog}/{landing_schema}/raw/support/glossary.csv"

print({"source_table": source_table, "index_name": index_name, "glossary_path": glossary_path})

# COMMAND ----------

glossary_df = (
    spark.read.option("header", True)
    .option("encoding", "UTF-8")
    .csv(glossary_path)
)
glossary_df.createOrReplaceTempView("gasentec_glossary_upload")

spark.sql(
    f"""
    CREATE OR REPLACE TABLE {source_table}
    TBLPROPERTIES (delta.enableChangeDataFeed = true)
    COMMENT 'LNG·재기화·BOG·FSRU·O&M 용어와 해석 규칙'
    AS SELECT * FROM gasentec_glossary_upload
    """
)

display(spark.table(source_table))

# COMMAND ----------

from databricks.ai_search.client import AISearchClient

client = AISearchClient()

try:
    client.get_endpoint(name=endpoint_name)
    print(f"기존 endpoint 사용: {endpoint_name}")
except Exception:
    client.create_endpoint(name=endpoint_name, endpoint_type="STANDARD")
    print(f"endpoint 생성 요청: {endpoint_name}")

# Endpoint가 ONLINE이 될 때까지 UI에서 상태를 확인합니다.

# COMMAND ----------

try:
    index = client.get_index(index_name=index_name)
    print(f"기존 index 사용: {index_name}")
except Exception:
    index = client.create_delta_sync_index(
        endpoint_name=endpoint_name,
        source_table_name=source_table,
        index_name=index_name,
        pipeline_type="TRIGGERED",
        primary_key="term_id",
        embedding_source_column="search_text",
        embedding_model_endpoint_name=embedding_model,
        columns_to_sync=[
            "term",
            "definition",
            "preferred_usage",
            "aliases",
            "example_question",
            "metric_or_field",
            "resolution_rule",
            "search_text",
        ],
    )
    print(f"index 생성 요청: {index_name}")

# COMMAND ----------

index = client.get_index(index_name=index_name)
index.sync()
print("Triggered sync를 시작했습니다. Catalog Explorer에서 ONLINE 상태를 확인하세요.")

# COMMAND ----------

index = client.get_index(index_name=index_name)
results = index.similarity_search(
    query_text="BOG와 boil-off rate의 의미를 알려줘",
    columns=["term_id", "term", "definition", "preferred_usage", "resolution_rule"],
    num_results=3,
    query_type="HYBRID",
)
display(results)
