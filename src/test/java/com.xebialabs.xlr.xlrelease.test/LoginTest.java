package com.xebialabs.xlr.xlrelease.test;

import com.xebialabs.pages.*;
import com.xebialabs.specs.BaseTest;
import org.testng.annotations.*;

public class LoginTest extends BaseTest {

    @BeforeMethod
    public void testStartUp(){
        System.out.println("called before method");
        LoginPage.login("admin","admin");
    }

    @Test
    public void OpenConfiguration_1(){
        MainMenu.clickMenu("Settings");
        SubMenu.clickSubMenu("Shared configuration");
        SharedConfigurationPage.openSharedConfiguration("Jenkins: Server");
        SharedConfigurationPropertiesPage.checkSharedConfigurationHeader("Jenkins");
    }

    @Test
    public void OpenConfiguration_2(){
        MainMenu.clickMenu("Settings");
        SubMenu.clickSubMenu("Shared configuration");
        SharedConfigurationPage.openSharedConfiguration("Git: Repository");
        SharedConfigurationPropertiesPage.checkSharedConfigurationHeader("Git");
    }

    @AfterMethod
    public void logout(){
        System.out.println("called after method");
        MainMenu.logout();
    }
}