import { render, screen } from "@testing-library/react";
import SearchBar from "../components/SearchBar";

test("shows search input", () => {
  const fn = vi.fn();
  render(<SearchBar onResults={fn} />);
  expect(screen.getByPlaceholderText(/Search by object label/i)).toBeInTheDocument();
});
