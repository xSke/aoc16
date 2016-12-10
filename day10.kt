val bots = mutableMapOf<Int, Bot>()
val output = mutableMapOf<Int, Int>()

enum class OutputType {
    OUTPUT,
    BOT
}

data class Output(val type: OutputType, val id: Int) {
    fun give(value: Int) {
        when (type) {
            OutputType.OUTPUT -> output[id] = value
            OutputType.BOT -> bots[id]!!.giveChip(value)
        }
    }
}

fun parseOutput(out: String): Output {
    val parts = out.split(" ")
    val id = parts[1].toInt()
    when {
        parts[0] == "output" -> return Output(OutputType.OUTPUT, id)
        parts[0] == "bot" -> return Output(OutputType.BOT, id)
    }
    throw RuntimeException()
}

data class Instruction(val low: Output, val high: Output)

data class Bot(var id: Int, val instruction: Instruction) {
    var values = mutableListOf<Int>()

    fun giveChip(number: Int) {
        values.add(number)
    }

    fun tick() {
        if (values.size >= 2) {
            val low = Math.min(values[0], values[1])
            val high = Math.max(values[0], values[1])

            values.removeAt(0)
            values.removeAt(0)

            instruction.low.give(low)
            instruction.high.give(high)
        }
    }
}

fun main(args: Array<String>) {
    var lines = generateSequence { readLine() }.toList()

    // Set up bots with their instructions
    val instructionRegex = Regex("bot (\\d+) gives low to ([\\w\\d\\s]+) and high to ([\\w\\d\\s]+)")
    lines.forEach {
        val match = instructionRegex.find(it)
        if (match != null) {
            val botId = match.groups[1]!!.value.toInt()

            val lowOut = parseOutput(match.groups[2]!!.value)
            val highOut = parseOutput(match.groups[3]!!.value)

            val bot = Bot(botId, Instruction(lowOut, highOut))
            bots[botId] = bot
        }
    }

    // Give some bots an initial value
    val valueRegex = Regex("value (\\d+) goes to bot (\\d+)")
    lines.forEach {
        val match = valueRegex.find(it)
        if (match != null) {
            val botId = match.groups[2]!!.value.toInt()
            val value = match.groups[1]!!.value.toInt()

            bots[botId]!!.giveChip(value)
        }
    }

    var theChosenOne: Bot? = null
    while (true) {
        val chosenOne = bots.values.find {
            val isChosen = it.values.size == 2 && it.values.contains(61) && it.values.contains(17)

            if (it.values.size >= 2) {
                it.tick()
            }

            isChosen
        }

        if (chosenOne != null) {
            theChosenOne = chosenOne
        }

        if (bots.values.all { it.values.size < 2 }) break
    }

    println(" - The chosen bot is bot #${theChosenOne?.id} -")
    println(" - Multiplying out #0, #1, and #2 gives ${output[0]!! * output[1]!! * output[2]!!}")
}