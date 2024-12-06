import time
import threading
import subprocess
from sparknlp.annotator import BertEmbeddings, Tokenizer
from sparknlp.base import DocumentAssembler
from pyspark.ml import Pipeline
import sparknlp
from pyspark.sql import SparkSession
from pyspark.sql import Row
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# Flag to control GPU monitoring
gpu_monitoring_active = True
gpu_utilization_data = []
# Function to monitor GPU utilization in parallel
def monitor_gpu_utilization():
    while gpu_monitoring_active:  # Check if the flag is active
        gpu_stats = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        utilization_match = re.search(r'(\d+)%\s+Default', gpu_stats)
        if utilization_match:
            gpu_utilization = int(utilization_match.group(1))
            gpu_utilization_data.append(gpu_utilization)

        # Check the flag every second within a longer sleep to allow for early exit
        for _ in range(1):  # Total of 5 seconds (adjust based on your need)
            if not gpu_monitoring_active:
                return
            time.sleep(1)


def update_plot(frame):
    plt.cla()  # Clear the previous plot
    plt.plot(gpu_utilization_data, label='GPU Utilization (%)')
    plt.ylim(0, 100)  # GPU utilization percentage is between 0 and 100
    plt.xlabel('Time (seconds)')
    plt.ylabel('GPU Utilization (%)')
    plt.title('Real-time GPU Utilization')
    plt.legend(loc='upper right')
# Start GPU monitoring in a separate thread
gpu_thread = threading.Thread(target=monitor_gpu_utilization)
gpu_thread.daemon = True  # This allows the thread to exit when the main program finishes
gpu_thread.start()

# Initialize the Spark session with GPU support
# spark = SparkSession.builder \
#     .appName("Spark NLP with GPU") \
#     .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp-gpu_2.12:5.0.0") \
#     .config("spark.executor.resource.gpu.amount", "1") \
#     .config("spark.task.resource.gpu.amount", "1") \
#     .config("spark.driver.memory", "16G") \
#     .config("spark.executor.memory", "16G") \
#     .config("spark.executor.cores", "4") \
#     .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
#     .config("spark.sql.execution.arrow.maxRecordsPerBatch", "2048") \
#     .config("spark.driver.extraJavaOptions", "-Dtensorflow.gpu=true") \
#     .getOrCreate()

spark = sparknlp.start(gpu=True)
# Start time tracking
start_time = time.time()

# Generate a large dataset to fully utilize the GPU
# Create a large dataset of strings (not arrays of strings)
text_data = ["This is a sample sentence for embedding."] * 1  # Repeat sentence to create a large dataset

# Create a DataFrame with single strings (not arrays)
data_df = spark.createDataFrame([Row(text=row) for row in text_data])

# Step 1: Define a document assembler
document_assembler = DocumentAssembler() \
    .setInputCol("text") \
    .setOutputCol("document")

# Step 2: Tokenize the text
tokenizer = Tokenizer() \
    .setInputCols(["document"]) \
    .setOutputCol("token")

# Step 3: Load a larger, more complex pretrained model to increase GPU usage
bert_embeddings = BertEmbeddings.pretrained("bert_large_uncased", "en") \
    .setInputCols(["document", "token"]) \
    .setOutputCol("embeddings") \
    .setCaseSensitive(False) \
    .setBatchSize(1)  # Increase batch size to use more GPU resources

# Step 4: Create a pipeline with document assembler, tokenizer, and embeddings
pipeline = Pipeline(stages=[document_assembler, tokenizer, bert_embeddings])

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_plot, interval=1000)
def run_pipeline():
    model = pipeline.fit(data_df)
    embedded_df = model.transform(data_df)
    # Show the embeddings (only the first 2 rows to avoid long output)
    embedded_df.select("embeddings.result").show(2, truncate=False)

pipeline_thread = threading.Thread(target=run_pipeline)
pipeline_thread.start()
#plt.show()



pipeline_thread.join()
# End time tracking
end_time = time.time()

# Calculate total time
total_time = end_time - start_time
print(f"Total execution time: {total_time:.2f} seconds")

# Stop GPU monitoring
gpu_monitoring_active = False

# Wait for the GPU monitoring thread to finish
gpu_thread.join()
print("GPU monitoring stopped.")
