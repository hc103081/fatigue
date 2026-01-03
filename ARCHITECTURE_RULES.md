# 專案程式架構規則

本文件旨在為 `fatigue` 專案提供一套程式架構規則，以確保程式碼的一致性、可維護性和可擴展性。

## 1. 模組職責 (Module Responsibilities)

*   **`main.py`**:
    *   作為專案的入口點。
    *   負責初始化所有核心組件（例如 `Camera`, `FaceAnalyzer`, `AlcoholSensor`, `Line_Api`, `MP3Player`）。
    *   管理主要執行緒（例如 `update_sensor_data`）。
    *   不應包含核心業務邏輯，應將其委派給各自的模組。
*   **`program/` 目錄**:
    *   包含所有核心業務邏輯模組。
    *   每個模組應具有單一職責原則 (Single Responsibility Principle)。
    *   例如：
        *   `camera.py`: 處理攝影機相關操作。
        *   `face_analyze.py`: 處理臉部偵測和疲勞分析。
        *   `alcohol.py`: 處理酒精感測器資料。
        *   `line_Api.py`: 處理 LINE Message API 互動。
        *   `mp3_player.py`: 處理音效播放。
        *   `logs.py`: 處理日誌記錄。
        *   `dataClass.py`: 定義專案中使用的資料結構。
*   **`deprecated_modules/` 目錄**:
    *   用於存放已棄用或不再使用的模組。
    *   這些模組應在 `main.py` 或其他相關文件中明確標記為棄用，並移除其初始化或使用。

## 2. 命名約定 (Naming Conventions)

*   **檔案/目錄**: 使用小寫蛇形命名法 (snake_case)，例如 `face_analyze.py`, `deprecated_modules`。
*   **類別 (Classes)**: 使用駝峰式命名法 (CamelCase)，例如 `FaceAnalyzer`, `Line_Api`, `MP3Player`。
*   **函數/方法 (Functions/Methods)**: 使用小寫蛇形命名法 (snake_case)，例如 `init_components`, `update_sensor_data`, `get_fatigue_score`。
*   **變數 (Variables)**: 使用小寫蛇形命名法 (snake_case)，例如 `fatigue_score`, `is_fatigued`, `access_token`。
*   **常數 (Constants)**: 使用大寫蛇形命名法 (SCREAMING_SNAKE_CASE)，例如 `LINE_CHANNEL_ACCESS_TOKEN`。

## 3. 環境變數管理 (Environment Variable Management)

*   所有敏感資訊（例如 API 金鑰、密鑰）和可配置的參數應透過環境變數進行管理。
*   使用 `python-dotenv` 庫在啟動時載入 `.env` 文件中的環境變數。
*   提供 `.env.example` 文件作為環境變數的範例和說明。
*   在程式碼中，使用 `os.getenv("VARIABLE_NAME")` 來存取環境變數。

## 4. 錯誤處理與日誌記錄 (Error Handling and Logging)

*   使用 `try-except` 區塊來捕獲和處理潛在的錯誤，以提高程式的健壯性。
*   使用 `program/logs.py` 模組進行統一的日誌記錄。
*   日誌訊息應包含足夠的上下文資訊，以便於問題診斷。
*   區分不同級別的日誌（例如 `debug`, `info`, `warning`, `error`）。

## 5. 程式碼註解與文件 (Code Comments and Documentation)

*   所有類別、函數和複雜的程式碼區塊都應包含清晰的註解或 Docstring，解釋其目的、參數、回傳值和任何特殊行為。
*   對於複雜的演算法或邏輯，應提供足夠的解釋。

## 6. 依賴管理 (Dependency Management)

*   所有專案依賴項應列在 `requirements.txt` 文件中，並指定確切的版本。
*   使用 `pip install -r requirements.txt` 來安裝依賴項。

## 7. 程式碼格式化 (Code Formatting)

*   遵循 PEP 8 規範進行程式碼格式化。
*   建議使用自動格式化工具（例如 Black, autopep8）來保持程式碼風格的一致性。

## 8. 測試 (Testing)

*   鼓勵為核心模組和功能編寫單元測試和整合測試，以確保程式碼的正確性。

## 9. 版本控制 (Version Control)

*   使用 Git 進行版本控制。
*   遵循清晰的提交訊息規範。
*   使用 `.gitignore` 文件忽略不應提交到版本控制的檔案（例如 `.env`, `__pycache__`）。
