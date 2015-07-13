/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

//package jena.examples.rdf ;

import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.vocabulary.*;

/** Tutorial 1 creating a simple model
 */

public class Tutorial01 extends Object {
    // some definitions
    static String personURI    = "http://somewhere/JohnSmith";
    static String fullName     = "John Smith";
      public static void main (String args[]) {
        org.apache.log4j.BasicConfigurator.configure(); 
        
        // create an empty model
        Model model = ModelFactory.createDefaultModel();

       // create the resource
       Resource johnSmith = model.createResource(personURI);

      // add the property
      johnSmith.addProperty(VCARD.FN, fullName);

      // list statements in model instance for John Smith
      StmtIterator iter = model.listStatements();

      System.out.println("\n***Beginning Output***\n");

      //print out the predicate, subject and object of each statement
      while (iter.hasNext()) {
          Statement stmt = iter.nextStatement();
          Resource subject = stmt.getSubject();
          Property predicate = stmt.getPredicate();
          RDFNode object = stmt.getObject();

          System.out.print(subject.toString());
          System.out.print(" " + predicate.toString() + " ");
          if (object instanceof Resource) {
              System.out.print(object.toString());
          } else {
              //object is a literal
              System.out.print("\"" + object.toString() + "\"");
          }

          System.out.println(" .");

          System.out.print("\n");
      }

      System.out.println("Done!");
      }
}
