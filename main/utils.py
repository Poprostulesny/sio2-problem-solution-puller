def redirect_to_tasks(url):
    desc_iter=0
    for i in range(len(url)-1):
        desc_iter = len(url)-i-2
        if(url[desc_iter]=='/'):
            break
    url_new =""
    for i in range(desc_iter):
        url_new=url_new + url[i]
    url_new+="/p"
    return(url_new)

def redirect_to_solutions(url):
    desc_iter=0
    for i in range(len(url)-1):
        desc_iter = len(url)-i-2
        if(url[desc_iter]=='/'):
            break
    url_new =""
    for i in range(desc_iter):
        url_new=url_new + url[i]
    url_new+="/submissions"
    return(url_new)

filename=newfile


        
