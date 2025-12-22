**1. Dependencies:**
> *   Use `opencv-python`, `mediapipe`, `requests`, `numpy`.
>
>**2. Core Logic:**
 **Face Mesh**: Initialize MediaPipe Face Mesh (refine_landmarks=True).
> *   **Buffer**: Create a `collections.deque(maxlen=60)` to store the last 2 seconds of video frames (assuming 30fps).
> *   **EAR Calculation**: Implement a function to calculate Eye Aspect Ratio.
> *   **Trigger Logic**:
>     *   If `EAR < 0.2` (eyes closed) for continuously 15 frames (0.5s):
>     *   **Action**: Retrieve 3 frames from the deque: index `[-45]` (Past), `[-10]` (Transition), `[-1]` (Now).
>     *   **Processing**: Resize them to 320x240 each and `cv2.hconcat` them into one image.
>     *   **API Call**: Encode the stitched image to Base64. Send HTTP POST to `process.env.SUPABASE_FUNCTION_URL`.
>     *   **Payload**: `{ "user_id": "driver_01", "image_base64": "...", "local_metrics": { "ear": ... } }`.
> *   **Cooldown**: Implement a 5-second cooldown after a trigger to prevent API spamming.
> *   **Async/Thread**: Run the API request in a separate `threading.Thread` so it doesn't freeze the video feed.
**3. Configuration:**
> *   Create a `.env` file template containing `SUPABASE_FUNCTION_URL` and `SUPABASE_ANON_KEY`.