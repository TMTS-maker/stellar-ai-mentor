import { Dialog, DialogContent } from "@/components/ui/dialog";
import { X } from "lucide-react";

interface VideoModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const VideoModal = ({ isOpen, onClose }: VideoModalProps) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl w-full p-0 overflow-hidden">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 z-50 rounded-full bg-background/80 p-2 hover:bg-background transition-colors"
        >
          <X className="h-4 w-4" />
        </button>
        <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
          <iframe
            src="https://drive.google.com/file/d/1DXKtstUJuKKHNFH0B30qjAiAo-0Mdfh8/preview"
            className="absolute top-0 left-0 w-full h-full"
            allow="autoplay"
            allowFullScreen
            title="Stellar AI Demo Video"
          />
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default VideoModal;
