import time
import logging
import functools # 1. Import functools

# Configure basic logging (you can customize this)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_tool_execution(tool_name):
    def decorator(func):
        @functools.wraps(func) # 2. Add this decorator to preserve the original function's docstring
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logging.info(f"🛠️ Starting tool: {tool_name}")
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logging.info(f"✅ Finished tool: {tool_name} in {duration:.2f}s")
            logging.info(f"📤 Output from {tool_name}: {result}")
            return result
        return wrapper
    return decorator