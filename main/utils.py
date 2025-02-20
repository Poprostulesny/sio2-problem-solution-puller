def get_base_url(url):
    desc_iter=0
    for i in range(len(url)-1):
        desc_iter = len(url)-i-2
        if(url[desc_iter]=='/'):
            break
    url_new =""
    for i in range(desc_iter):
        url_new=url_new + url[i]
    return url_new
def redirect_to_tasks(url):
    url_new = get_base_url(url)
    url_new+="/p"
    return(url_new)

def redirect_to_solutions(url):
    url_new = get_base_url(url)
    url_new+="/submissions"
    return(url_new)




        
