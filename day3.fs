let firstThreeToTuple (a : _[]) = (a.[0], a.[1], a.[2])

let fst(a, _, _) = a
let snd (_, b, _) = b
let trd (_, _, c) = c
let verticalToTuple (a : (int*int*int) list) = [
    (fst a.[0], fst a.[1], fst a.[2]);
    (snd a.[0], snd a.[1], snd a.[2]);
    (trd a.[0], trd a.[1], trd a.[2]);
]
let validTriangle (a, b, c) = a + b > c && a + c > b && b + c > a

[<EntryPoint>]
let main args = 
    printfn "Taking input from stdin, Ctrl-Z to stop"

    let lines: string list =
        Seq.initInfinite (fun _ -> System.Console.In.ReadLine())
        |> Seq.takeWhile(fun line -> line <> null)
        |> Seq.toList

    let numbersHorizontally: (int * int * int) list =
        lines
        |> List.map (fun x -> 
           x.Split ([|' '|], System.StringSplitOptions.RemoveEmptyEntries)
           |> Array.map int
           |> firstThreeToTuple)

    let numbersVertically: (int * int * int) list =
        numbersHorizontally
        |> List.chunkBySize 3
        |> List.collect (fun x ->
            x 
            |> verticalToTuple)
        
    let validTris numbers =
        numbers
        |> Seq.filter validTriangle
        |> Seq.length

    printfn " - %i triangles are valid -" (validTris numbersHorizontally)
    printfn " - %i triangles are valid, vertically -" (validTris numbersVertically)
    0