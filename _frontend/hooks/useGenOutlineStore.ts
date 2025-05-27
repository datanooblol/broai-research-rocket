import { create } from "zustand";

type GenOutline = {
  markdown: string;
  setMarkdown: (newMarkdown: string) => void;
};

export const useGenOutlineStore = create<GenOutline>((set) => ({
  markdown: "",
  setMarkdown: (newMarkdown) => set({ markdown: newMarkdown}),
}));
