/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//package ldap_api;

import java.util.Hashtable;
import javax.naming.Context;
import javax.naming.NamingEnumeration;
import javax.naming.directory.Attributes;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;

/**
 *
 * @author Dheerendra Yadav
 */
public class LDAP_API {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        System.out.print(ldapSearch(args[0]));        
    }
    public static String ldapSearch(String userid)
    {
        String dn="uid=searchAPI, ou=office, ou=People, dc=iitj,dc=ac,dc=in"; 
        String ldapURL = "ldap://172.16.100.6:389";
        Hashtable<String, String> env = new Hashtable<String, String>();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, ldapURL);
        
        env.put(Context.SECURITY_AUTHENTICATION, "simple");
        env.put(Context.SECURITY_PRINCIPAL, dn);                 
        env.put(Context.SECURITY_CREDENTIALS, "s3@rchAPI");
        boolean result=false;
        // Create the initial context
        String name="";
        dn="";
        try
        {
            DirContext ctx = new InitialDirContext(env);
            
            SearchControls constraints = new SearchControls();
            constraints.setSearchScope(SearchControls.SUBTREE_SCOPE);
            String[] attrIDs = {"sn","mail","uid", "cn", "entrydn", "givenName", "ou"};
            constraints.setReturningAttributes(attrIDs);
            
            NamingEnumeration answer = ctx.search("ou=People, dc=iitj, dc=ac, dc=in", "uid="+userid, constraints);
            if (answer.hasMore()) 
            {
                Attributes attrs = ((SearchResult) answer.next()).getAttributes();
                dn=attrs.get("entrydn").toString();
                name=attrs.get("givenName").toString().replaceAll("givenName:", "");
                name=name.trim();
                return dn.substring(dn.indexOf(",ou")+1, dn.indexOf(",dc")).split(",")[0].split("=")[1];                
            }
            else
                return "0";
        }
        catch(Exception e)
        {
            return "Exception: "+e;
        }        
            
    }
    
}
