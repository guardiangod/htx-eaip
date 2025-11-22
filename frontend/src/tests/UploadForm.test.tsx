import { render, screen, fireEvent } from "@testing-library/react";
import UploadForm from "../components/UploadForm";

test("renders upload form", () => {
  const fn = vi.fn();
  render(<UploadForm onJobCreated={fn} />);
  expect(screen.getByText(/Upload Media/i)).toBeInTheDocument();
});
