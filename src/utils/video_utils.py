from src.models.gemini_client import MedAIclient
import cv2

client = MedAIclient()

def extract_key_frames(video_path: str, num_frames: int = 3):
    """
    TAKE A VIDEO → PICK FEW FRAMES → SAVE AS IMAGES.
    """

    frames = []  # this will store paths of saved images

    try:
        # 1) Load the video file
        cap = cv2.VideoCapture(video_path)

        # 2) Find how many total frames are inside the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 3) Decide how many frames to skip between each selected frame
        # Example: if video has 300 frames and we need 3 → step = 100
        step = max(1, total_frames // num_frames)

        # 4) Loop through the video using the step value
        for i in range(0, total_frames, step):

            # Move the video reader to frame 'i'
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)

            # Read that frame
            ret, frame = cap.read()

            # If frame is read successfully, save it as image
            if ret:
                frame_path = f"{video_path}_frame_{i}.jpg"
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)

            # Stop if we already got required frames
            if len(frames) >= num_frames:
                break

        cap.release()  # close the video file
        return frames  # return list of frame image paths

    except Exception as e:
        return f" Error extracting video frames: {str(e)}"

def analyze_posture_from_frames(frame_paths: list,progress_callback = None):
    """
    TAKE IMAGES → SEND TO GEMINI → GET POSTURE ANALYSIS.
    """
    total_frames = len(frame_paths)
    analysis = ""  # store combined result

    try:
        for idx , frame in enumerate(frame_paths):

            # Prompt given to Gemini
            prompt = """
            You are a physiotherapy posture assistant.
            Analyze the person's posture in this image.
            - Identify basic posture issues
            - Only give fitness suggestions
            - No medical diagnosis
            """

            # Send image + prompt to Gemini
            result = client.analyze_image(frame, prompt)

            # Add result to the final analysis string
            analysis += f"\n📌 Frame {idx+1} Analysis:\n{result}\n"
            
            if progress_callback:
                progress_callback((idx+1)/total_frames)

        return analysis.strip()  # remove extra newlines and return

    except Exception as e:
        return f" Error analyzing posture: {str(e)}"

def analyze_video_posture(video_path: str):
    """
    FULL PROCESS:
    1) Extract frames from video
    2) Send them to Gemini for analysis
    3) Return the final posture report
    """

    # Step 1: extract frames
    frames = extract_key_frames(video_path)

    # If frames is a string → it means an error occurred
    if isinstance(frames, str):
        return frames

    # Step 2: analyze the extracted frames
    return analyze_posture_from_frames(frames)
