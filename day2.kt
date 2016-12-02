data class Point(val x: Int, val y: Int)

fun execute(pad: String, instructions: List<String>, start: Point): String {
    val rows = pad.split("/")

    val (pos, buffer) = instructions.fold(Pair(start, "")) { (pos, buffer), line ->
        val pos = line.fold(pos) { pos, instruction ->
            val nextPos = when (instruction) {
                'U' -> pos.copy(y = pos.y - 1)
                'D' -> pos.copy(y = pos.y + 1)
                'L' -> pos.copy(x = pos.x - 1)
                'R' -> pos.copy(x = pos.x + 1)
                else -> pos
            }

            when {
                nextPos.x < 0 || nextPos.y < 0 || nextPos.x >= rows[0].length || nextPos.y >= rows.size -> pos
                rows[nextPos.y][nextPos.x].isWhitespace() -> pos
                else -> nextPos
            }
        }
        Pair(pos, buffer + rows[pos.y][pos.x])
    }
    return buffer
}

fun main(args: Array<String>) {
    val instructions = mutableListOf<String>()
    while (true) {
        val line = readLine() ?: break
        instructions.add(line)
    }

    val part1 = execute("123/456/789", instructions, Point(1, 1))
    val part2 = execute("  1  / 234 /56789/ ABC /  D  ", instructions, Point(0, 2))
    println(" - Your imagined bathroom code is %s -".format(part1))
    println(" - The actual bathroom code is %s -".format(part2))
}