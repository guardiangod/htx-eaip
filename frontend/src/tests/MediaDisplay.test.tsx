import { render, screen } from "@testing-library/react";
import VideoList from "../components/VideoList";

test("video list renders titles", () => {
  render(<VideoList videos={[{ id: 1, filename: "test.mp4", created_at: "", frames: [], summary: "" }]} />);
  expect(screen.getByText("test.mp4")).toBeInTheDocument();
});
