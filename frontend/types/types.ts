export interface Transcript {
  start: number;
  duration: number;
  text: string;
}

export interface TranscriptsProps {
  transcriptRef: React.RefObject<HTMLDivElement | null>;
  transcripts: Transcript[];
  currentTime: number;
}

export interface UrlProps {
  url: string;
  setUrl: (url: string) => void;
  handleSubmit: (e: React.MouseEvent<HTMLButtonElement>) => Promise<void>;
  loading: boolean;
}

export interface ErrorProps {
  error: string;
}
