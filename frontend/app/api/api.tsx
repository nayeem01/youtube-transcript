export const fetchTranscript = async (url: string) => {
  const apiIP = process.env.API_IP;
  try {
    const response = await fetch(`http://${apiIP}:8000/get-transcript/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });
    if (!response.ok)
      throw new Error(
        "Error fetching transcript: Could not retrieve a transcript for the video"
      );

    const data = await response.json();
    const parsedTranscript = JSON.parse(data.transcript);

    return {
      videoId: data.video_id,
      transcript: parsedTranscript,
    };
  } catch (err) {
    if (err instanceof Error) {
      throw new Error(err.message);
    }
    throw new Error("An unknown error occurred");
  }
};
