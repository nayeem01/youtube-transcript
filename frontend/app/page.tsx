"use client";

import { useState, useEffect, useRef } from "react";
import { Container } from "@mui/material";

import { Transcript } from "../types/types";

import ErrorMessage from "@/components/ErrorMessage";
import Transcripts from "@/components/Transcripts";
import YoutubePlayer from "@/components/YoutubePlayer";
import Url from "@/components/Url";

import { fetchTranscript } from "./api/api";

export default function Home() {
  const [url, setUrl] = useState("");
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [videoId, setVideoId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentTime, setCurrentTime] = useState(0);

  const playerRef = useRef<YT.Player | null>(null);
  const transcriptRef = useRef<HTMLDivElement>(null);
  const [isPlayerReady, setIsPlayerReady] = useState(false);

  const loadYouTubeAPI = () => {
    const tag = document.createElement("script");
    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName("script")[0];
    if (firstScriptTag.parentNode) {
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
  };

  useEffect(() => {
    if (!videoId) return;

    if (!window.YT) {
      loadYouTubeAPI();
    }

    window.onYouTubeIframeAPIReady = () => {
      playerRef.current = new YT.Player("youtube-player", {
        videoId: videoId,
        playerVars: {
          autoplay: 1,
          controls: 1,
        },
        events: {
          onStateChange: onPlayerStateChange,
        },
      });
    };

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
      }
    };
  }, [videoId]);

  const onPlayerStateChange = (event: YT.OnStateChangeEvent) => {
    if (event.data === YT.PlayerState.ENDED) {
      setIsPlayerReady(true);
    }

    const interval = setInterval(() => {
      if (playerRef.current) {
        const time = playerRef.current.getCurrentTime();
        setCurrentTime(time);
      }
    }, 500);

    return () => clearInterval(interval);
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setTranscripts([]);
    setVideoId("");

    try {
      const { videoId, transcript } = await fetchTranscript(url);
      setVideoId(videoId);
      setTranscripts(transcript);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isPlayerReady && playerRef.current) {
      playerRef.current.playVideo();
    }
  }, [isPlayerReady]);

  useEffect(() => {
    if (transcriptRef.current && transcripts.length > 0) {
      const activeIndex = transcripts.findIndex(
        (transcript) =>
          currentTime >= transcript.start &&
          currentTime < transcript.start + transcript.duration
      );

      if (activeIndex !== -1) {
        const activeElement = transcriptRef.current.children[activeIndex];
        if (activeElement) {
          activeElement.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
        }
      }
    }
  }, [currentTime, transcripts]);

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Url
        url={url}
        setUrl={setUrl}
        handleSubmit={handleSubmit}
        loading={loading}
      />

      {error && <ErrorMessage error={error} />}

      {videoId && <YoutubePlayer />}

      {transcripts.length > 0 && (
        <Transcripts
          transcriptRef={transcriptRef}
          transcripts={transcripts}
          currentTime={currentTime}
        />
      )}
    </Container>
  );
}
