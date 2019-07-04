# Stanley Cup Champion Webscraper

## Setup
Before copying the below code into the VBA editor in Excel ensure that the following references are selected:<br>
* **Microsoft HTML Object Library**<br>
* **Microsoft Internet Controls**

```VBA
Sub StanleyCupChamp1927_2019()

    Dim ieObj As InternetExplorer
    Dim htmlEle As IHTMLElement
    Dim i As Integer

    i = 1

    Set ieObj = New InternetExplorer

    ' comment out below to hide browser instance
    'ieObj.Visible = True


    ieObj.navigate "https://en.wikipedia.org/wiki/List_of_Stanley_Cup_champions#NHL_champions_(since_1927)"


' to allow webpage to load
    Application.Wait Now + TimeValue("00:00:03")

' loop statement to parse webpage and paste into active sheet

    For Each htmlEle In ieObj.document.getElementsByClassName("wikitable sortable jquery-tablesorter")(2).getElementsByTagName("tr")

'to account for the 04/05 lockout season row in table an IF/Else Statement has been created

        If htmlEle.Children(0).textContent = "2005" Then
            With ActiveSheet
            .Range("A" & i).Value = htmlEle.Children(0).textContent
            .Range("B" & i).Value = htmlEle.Children(1).textContent
            End With
        Else
            With ActiveSheet
            .Range("A" & i).Value = htmlEle.Children(0).textContent
            .Range("B" & i).Value = htmlEle.Children(1).textContent
            .Range("C" & i).Value = htmlEle.Children(2).textContent
            .Range("D" & i).Value = htmlEle.Children(3).textContent
            .Range("E" & i).Value = htmlEle.Children(4).textContent
            .Range("F" & i).Value = htmlEle.Children(5).textContent
            .Range("G" & i).Value = htmlEle.Children(6).textContent
            End With
        End If

        i = i + 1

    Next htmlEle

End Sub
```
