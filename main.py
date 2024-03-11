import bs4
import requests


def main():
    input_txt = open("input.txt", "r", encoding="utf-8")
    lines = input_txt.readlines()
    output = ""
    number_of_lines = len(lines)

    for line_number, line in enumerate(lines):
        line_strip = line.strip()

        if not line_strip:
            continue

        line_split = line_strip.split()

        if len(line_split) != 2:
            continue

        word = line_split[0].strip()
        part_of_speech = line_split[1].strip("()")

        if part_of_speech == "j":
            part_of_speech = "adj"
        elif part_of_speech == "r":
            part_of_speech = "adv"

        response = requests.get(f"https://www.google.com/search?q={word}+definition")
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        definitions = soup.body.find_all(class_="Ap5OSd")

        if not definitions:
            continue

        for index, definition in enumerate(definitions):
            span = definition.find("span", class_="r0bn4c rQMQod")

            if not span:
                continue

            string = str(span.string).strip().split()

            if len(string) != 1:
                continue

            if not string[0].startswith(part_of_speech):
                continue

            definition = definitions[index + 1].find("div", class_="BNeawe s3v9rd AP7Wnd")
            output += f"{word.capitalize()} ({part_of_speech}): {definition.string}\n"
            break

        print(f"{line_number + 1}/{number_of_lines} ({(line_number + 1) / number_of_lines * 100}%)")

    input_txt.close()

    output_txt = open("output.txt", "w", encoding="utf-8")
    output_txt.write(output)
    output_txt.close()


if __name__ == "__main__":
    main()
