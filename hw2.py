def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']

    assert (isinstance(result, int))  # Updated. Safety check for the type of result

    print(
        f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if
                 country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format:
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)



def getCountry(file_name, competitor_id):
    file = open(file_name, 'r')
    i = 0
    lines = file.readlines()
    while not i == len(lines):
        line=lines[i].split()
        if line[0] == 'competitor':
            if line[1] == competitor_id:
                file.close()
                return line[2]
        i=i+1


def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments:
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country,
                'result': result}
    '''
    competitors_in_competitions = []
    # TODO Part A, Task 3.4
    file = open(file_name, 'r')
    i=0
    lines = file.readlines()
    while not i== len(lines):
        splitted = lines[i].split()

        if splitted[0] == "competition":
            dict = {'competition name': splitted[1], 'competition type': splitted[3], 'competitor id': splitted[2],
                    'competitor country': getCountry(file_name, splitted[2]), 'result': int(splitted[4])}
            competitors_in_competitions.append(dict)
           # dict={}
        i = i+1

    file.close()

    return competitors_in_competitions

def findChamps (competitors_in_competitions, comp_name,comp_type):
    i=0
    results=[]
    while not i==len(competitors_in_competitions):
        if competitors_in_competitions[i]['competition name']== comp_name:
            results.append(competitors_in_competitions[i]['result'])
        i=i+1
    if comp_type == 'untimed':
        results = sorted(results,reverse=True)
    else:
        results = sorted(results)


    k=0

    return_list = [comp_name,'undef_country','undef_country','undef_country']
    #print(return_list)
    while k<3 and not k == len (results):
        j = 0
        while not j == len(competitors_in_competitions) :
            if competitors_in_competitions[j]['competition name'] == comp_name and competitors_in_competitions[j]['result']== results[k]:

                return_list[k+1] = competitors_in_competitions[j]['competitor country']
            j = j+1
        k=k+1

    return return_list


def checkToDelete(competitors_in_competitions,comp_id,comp_name):
    i=0
    counter=0
    li=[]
    while not i==len(competitors_in_competitions):
        li.append(1)
        if competitors_in_competitions[i]["competition name"]==comp_name and competitors_in_competitions[i]["competitor id"]==comp_id:
            counter=counter+1
        if counter>1:
            return 1
        i=i+1
    return 0



def delete_cheaters(competitors_in_competitions,competition_names):
    ifdeleted=0
    for k,v in competition_names.items():
        i=0
        newlist=[]
        while not i==len(competitors_in_competitions):
            newlist.append(1)
            if checkToDelete(competitors_in_competitions,competitors_in_competitions[i]["competitor id"],k)==1:
                j=0
                deletedId = competitors_in_competitions[i]["competitor id"]
                while not j==len(competitors_in_competitions):
                    if competitors_in_competitions[j]["competition name"]==k and deletedId==competitors_in_competitions[j]["competitor id"]:
                        competitors_in_competitions.pop(j)
                        ifdeleted=1

                    if not ifdeleted==1:
                        j=j+1
                    ifdeleted=0

            i=i+1

    return competitors_in_competitions





def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists).
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    '''
    competitions_champs = []
    # TODO Part A, Task 3.5

    competitions_dict = {}
    i=0
    while not i== len(competitors_in_competitions):
        name= competitors_in_competitions[i]['competition name']
        type=competitors_in_competitions[i]['competition type']
        competitions_dict[name]=type
        i= i+1

    competitors_in_competitions= delete_cheaters(competitors_in_competitions,competitions_dict)

    i = 0
    while not i == len(competitors_in_competitions):
        name = competitors_in_competitions[i]['competition name']
        type = competitors_in_competitions[i]['competition type']
        competitions_dict[name] = type
        i = i + 1

    for name in competitions_dict.keys():
        temp_list = findChamps(competitors_in_competitions,name, competitions_dict[name])
        if not temp_list[1] == 'undef_country' :
            competitions_champs.append(temp_list)

    return competitions_champs

def partA(file_name='input.txt', allow_prints=True):

    competitors_in_competitions = readParseData(file_name)
    if allow_prints:

        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)


    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)

    return competitions_results


def partB(file_name='input.txt'):
    competitions_results = partA(file_name, allow_prints=False)
    # TODO Part B
    import Olympics
    o = Olympics.OlympicsCreate()
    j=0
    while not j== len(competitions_results):
        Olympics.OlympicsUpdateCompetitionResults(o,str(competitions_results[j][1]),str(competitions_results[j][2]),str(competitions_results[j][3]))
        j=j+1
    Olympics.OlympicsWinningCountry(o)
    Olympics.OlympicsDestroy(o)

if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.

    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''
    file_name = 'input.txt'

    partA(file_name)
    partB(file_name)