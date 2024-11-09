import re, requests, bs4

headers: dict[str, str] = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}

#--> Buat dapetin semua file (misal kontennya berupa folder)
class PoopFile():

    #--> Konstruktor
    def __init__(self) -> None:

        self.file : list = []
        self.r = requests.Session()
        self.headers: dict[str,str] = headers

    #--> Redirect ke URL asli (yg msh aktif)
    def redirect(self, url:str) -> None:
        return(self.r.head(url, headers=self.headers, allow_redirects=True).url)

    #--> Dapetin semua file
    def getAllFile(self, url:str) -> None:

        #--> Get 1 : Mendapat redirect URL (asli)
        base_url : str = self.redirect(url)

        #--> Get 2 : Mendapat response text HTML
        req : object = self.r.get(base_url, headers=self.headers)
        self.domain : str = req.url.replace('//','/').split('/')[1]

        #--> Rapikan response
        soup : str = bs4.BeautifulSoup(req.text.replace('\\','').replace('\n',''), 'html.parser').prettify().replace('\n', '').replace('  ', '').replace('> <','><')

        #--> Sortir semua file
        type_url : str = req.url.replace('//','/').split('/')[2].lower()

        #--> Kalau konten berupa folder
        if type_url == 'f':
            list_page = list(dict.fromkeys(self.getAllPage(soup)))
            for i in list_page:
                try:
                    req  : object = self.r.get(i, headers=self.headers)
                    soup : str = bs4.BeautifulSoup(req.text.replace('\\','').replace('\n',''), 'html.parser').prettify().replace('\n', '').replace('  ', '').replace('> <','><')
                    self.multiFile(soup)
                except: continue

        #--> Kalau konten berupa file tunggal
        elif type_url == 'd':
            self.singleFile(req.url)

    #--> Mendapat semua page
    def getAllPage(self, soup:str) -> list[str]:
        return([f'https://{self.domain}{i}'for i in re.findall(r'<a class="page-link" href="(.*?)">.*?</a>',str(soup))])

    #--> Jika konten berisi banyak video
    def multiFile(self, soup:str) -> None:
        list1 : list[str] = re.findall(r'<div class=\".*?\">(.*?)</div>',str(soup))
        list2 : list[str] = [string for string in list1 if 'strong' in string]
        for i in list2:
            try:
                id    : str = re.search(r'href="(.*?)"',str(i)).group(1).split('/')[-1]
                name  : str = re.search(r'<strong>(.*?)</strong>',str(i)).group(1).strip()
                image : str = re.search(r'src="(.*?)"',str(i)).group(1)
                item  : dict[str,str] = {'domain':self.domain, 'id':id, 'name':name, 'image':image}
                self.file.append(item)
            except: continue

    #--> Jika konten berisi single video
    def singleFile(self, url:str) -> None:
        try:
            req   : object = self.r.get(url, headers=self.headers)
            soup  : str = bs4.BeautifulSoup(req.text.replace('\\','').replace('\n',''), 'html.parser').prettify().replace('\n', '').replace('  ', '').replace('> <','><')
            id    : str = url.replace('//','/').split('/')[-1].split('?')[0]
            name  : str = re.search(r'<h4>(.*?)</h4>',str(soup)).group(1).strip()
            image : str = re.search(r'<img alt=\".*?\" class=\".*?\" src="(.*?)"',str(soup)).group(1)
            item  : dict[str,str] = {'domain':self.domain, 'id':id, 'name':name, 'image':image}
            self.file.append(item)
        except: pass

#--> Buat dapetin link download & streaming dari masing-masing file
class PoopLink():

    #-> Konstruktor
    def __init__(self) -> None:

        self.link = ''
        self.r = requests.Session()
        self.headers: dict[str,str] = headers

    #--> Redirect ke URL asli (yg msh aktif)
    def redirect(self, url:str) -> None:
        return(self.r.head(url, headers=self.headers, allow_redirects=True).url)

    #--> Dapetin link download & streaming
    def getLink(self, domain:str, id:str) -> None:

        try:

            #--> Get 1 : Mendapat redirect URL (asli)
            url1 : str = self.redirect(f'https://{domain}/p0?id={id}')

            #--> Get 2 : Mendapat headers & redirect URL 2
            req2 : object = self.r.get(url1, headers=self.headers)
            soup : str = bs4.BeautifulSoup(req2.text.replace('\\','').replace('\n',''), 'html.parser').prettify().replace('\n', '').replace(' ', '').replace('> <','><').replace("'", '"')
            url2 : str = re.search(r'returnfetch\("(.*?)"',str(soup)).group(1).strip()
            auth : str = re.search(r'"Authorization":"(.*?)"',str(soup)).group(1).strip()

            #--> Get 3 : Mendapat direct download & streaming URL
            head : dict[str, str] = {'Authorization':auth}
            req3 : object = self.r.get(url2, headers={**self.headers, **head}).json()
            self.link : str = req3.get('direct_link', '')

        except: pass

#--> Buat ngetest aja
def Test() -> None:

    #--> Contoh Link Poop
    list_url : list[str] = ['https://poop.vin/d/LPxbX8Mn4KZ', 'https://poop.pm/f/t8e12zcx7ra', 'https://poop.pm/f/p6mqkgysdr0', 'https://poop.pm/f/be20crhis8g', 'https://poop.pm/f/WTdgWsSnlnv']
    url : str = list_url[0]

    #--> Contoh ID Video
    list_id : list[str] = ['LPxbX8Mn4KZ', 'ggvl28sr6tuu', 'sjg5d1abyi5e', '6yz2q62slsir', 'JJOXFuOZoJL']
    id : str = list_id[0]

    #--> Dapetin data semua file (params=[url]) (response=[domain, id, nama, image])
    PF = PoopFile()
    PF.getAllFile(url)
    print(PF.file)

    #--> Contoh domain
    domain = 'poop.run'

    #--> Dapetin link dari masing2 video (params=[domain, id]) (response=[link])
    PL = PoopLink()
    PL.getLink(domain, id)
    print(PL.link)

if __name__ == '__main__':
    Test()

# open('test_poop.txt','w',encoding='utf-8').write(str(soup))