---
name: "prd-guide"
description: "Principles of writing unambiguous Product Requirement Documents."
---

# Product Requirements Document (PRD) Guide

## Overview

You are a senior product manager and technical specification expert. Create a comprehensive Product Requirements Document (PRD) that clearly defines what to build, why to build it, and how success will be measured.

## INPUT REQUIREMENTS

Please provide the following information:

### Product Overview

- **Product Name**: [What you are building]
- **Product Type**: [Web app, mobile app, feature, integration, etc.]
- **Target Users**: [Primary user segments]
- **Core Problem**: [Main problem this solves]
- **Success Metrics**: [How you will measure success]

### Business Context

- **Business Goals**: [Revenue, user growth, retention, etc.]
- **Strategic Priority**: [High, Medium, Low and why]
- **Market Opportunity**: [Size and timing]
- **Competitive Landscape**: [How this differentiates]
- **Resource Constraints**: [Timeline, budget, team limitations]

### User Research

- **User Personas**: [Primary and secondary users]
- **User Pain Points**: [Current problems and frustrations]
- **User Goals**: [What users want to achieve]
- **User Workflows**: [Current process and ideal future state]
- **User Feedback**: [Insights from interviews, surveys, support tickets]

### Technical Context

- **Current Architecture**: [Existing systems and constraints]
- **Technical Dependencies**: [Required integrations or prerequisites]
- **Performance Requirements**: [Speed, scalability, reliability needs]
- **Security Requirements**: [Data protection and compliance needs]
- **Platform Requirements**: [Web, mobile, desktop compatibility]

## OUTPUT DELIVERABLES

Create a complete Product Requirements Document:

### 1. Executive Summary

**Product Vision:**

- One-sentence description of the product
- Target user and use case
- Key differentiator and value proposition
- Definition of success and metrics

**Strategic Alignment:**

- Business objectives this supports
- User problems this solves
- Market opportunity and timing
- Competitive advantage gained

**Resource Requirements:**

- Development effort estimate
- Timeline and key milestones
- Team members and skills needed
- Budget and resource allocation

### 2. Problem Statement and Opportunity

**Problem Definition:**

- Detailed description of user pain points
- Quantified impact of current problems
- Evidence supporting the existence of the problem
- User research and data supporting the claims

**Opportunity Analysis:**

- Market size and growth potential
- Size and characteristics of the user segment
- Revenue opportunity and business impact
- Competitive gap this addresses

**Success Criteria:**

- Primary success metrics and targets
- Secondary metrics to monitor
- Expected user behavior changes
- Anticipated business outcomes

### 3. User Requirements and Stories

**Primary User Personas:**

- Detailed persona descriptions
- User goals and motivations
- Current workflow and pain points
- Success criteria for each persona

**User Journey Mapping:**

- Current state user journey
- Proposed future state journey
- Key touchpoints and interactions
- Pain points and opportunity areas

**Core User Stories:**

- Epic-level user stories
- Detailed feature-level stories
- Acceptance criteria for each story
- Priority and dependency mapping

**Examples of User Stories:**

- As a [type of user], I want to [capability] so that [benefit]
- Given [context], when [action], then [result]
- Acceptance criteria with measurable outcomes

### 4. Functional Requirements

**Core Features (Must-Haves):**

- Detailed feature descriptions
- User workflows and interactions
- Input/output specifications
- Business logic requirements

**Secondary Features (Nice-to-Haves):**

- Enhancement opportunities
- Future iteration possibilities
- Optional functionality
- Competitive differentiation features

**Feature Prioritization:**

- MoSCoW Method (Must, Should, Could, Won't)
- Impact vs. Effort matrix
- User value and business value scoring
- Dependency and sequencing requirements

### 5. Technical Requirements

**Architecture Specifications:**

- System architecture overview
- Component and service definitions
- Data flow and integration points
- Scalability and performance requirements

**API Requirements:**

- Endpoint specifications
- Request/response formats
- Authentication and authorization
- Rate limiting and error handling

**Data Requirements:**

- Data model and schema definitions
- Data sources and integrations
- Data validation and constraints
- Privacy and security requirements

**Performance Specifications:**

- Response time requirements
- Throughput and capacity needs
- Availability and reliability targets
- Scalability and growth projections

### 6. User Experience Requirements

**Design Principles:**

- User experience philosophy
- Design system and style guide
- Accessibility requirements
- Usability standards and guidelines

**Interface Requirements:**

- Screen layouts and wireframes
- Navigation and information architecture
- Interactive elements and behaviors
- Responsive design requirements

**Usability Criteria:**

- Task completion success rates
- User satisfaction scores
- Learning curve and onboarding
- Error prevention and recovery

### 7. Non-Functional Requirements

**Security Requirements:**

- Authentication and authorization
- Encryption and data protection
- Compliance requirements (GDPR, HIPAA, etc.)
- Security testing and validation

**Performance Requirements:**

- Page load times and response speeds
- Concurrent user capacity
- Database performance requirements
- Network and bandwidth considerations

**Reliability Requirements:**

- Uptime and availability targets
- Error rate and fault tolerances
- Backup and disaster recovery
- Monitoring and alerting systems

**Scalability Requirements:**

- User growth projections
- Data volume growth expectations
- Geographic expansion requirements
- Infrastructure scaling capabilities

### 8. Success Metrics and Analytics

**Key Performance Indicators:**

- User acquisition and activation
- User engagement and retention
- Feature adoption and usage
- Business metrics and revenue impact

**Analytics Implementation:**

- Tracking requirements and events
- Dashboard and reporting needs
- A/B testing capabilities
- User behavior analysis tools

**Success Measurement:**

- Baseline metrics and benchmarks
- Target goals and timelines
- Success criteria and thresholds
- Review and optimization process

### 9. Implementation Plan

**Development Phases:**

- MVP scope and timeline
- Iterative development phases
- Feature release strategy
- Risk mitigation plans

**Resource Allocation:**

- Development team requirements
- Design and UX resources
- QA and testing needs
- DevOps and infrastructure support

**Timeline and Milestones:**

- Project kickoff and discovery
- Design and prototyping phase
- Development sprints and releases
- Testing and quality assurance
- Launch and post-launch optimization

### 10. Risk Assessment and Mitigation

**Technical Risks:**

- Architecture and scalability challenges
- Integration complexity and dependencies
- Performance and reliability concerns
- Security and compliance risks

**Business Risks:**

- Time to market and competition
- User adoption and engagement
- Resource availability and constraints
- Regulatory and legal considerations

**Mitigation Strategies:**

- Risk probability and impact assessment
- Preventive measures and contingencies
- Monitoring and early warning systems
- Response plans and alternatives

```markdown
## PRD TEMPLATE STRUCTURE

### 1. Executive Summary

- **Product**: [Your Product]
- **Owner**: [Product Manager]
- **Status**: [Draft/Review/Approved]
- **Last Updated**: [Date]

- **Vision**: [One-sentence product description]
- **Success Metrics**: [Primary KPI and target]

### 2. Problem and Opportunity

- **Problem**: [User problem being solved]
- **Opportunity**: [Business opportunity and market size]
- **Solution**: [High-level solution approach]

### 3. User Requirements

- **Primary Users**: [Target user segments]
- **Key Use Cases**: [Top 3-5 user scenarios]
- **Success Criteria**: [How users will measure success]

### 4. Product Requirements

**Must-Have Features:**

- **[Feature 1]**: [Description and acceptance criteria]
- **[Feature 2]**: [Description and acceptance criteria]
- **[Feature 3]**: [Description and acceptance criteria]

**Nice-to-Have Features:**

- **[Enhancement 1]**: [Description and priority]
- **[Enhancement 2]**: [Description and priority]

### 5. Technical Specifications

- **Architecture**: [High-level technical approach]
- **Dependencies**: [Required systems and integrations]
- **Performance**: [Speed, scale, and reliability requirements]

### 6. Success Metrics

- **Primary**: [Main success metric and target]
- **Secondary**: [Supporting metrics to track]
- **Timeline**: [When to measure and review]
```

## QUALITY CHECKLIST

Before finalizing the PRD, ensure that:

- ✓ The problem is clearly defined with evidence
- ✓ The solution aligns with user needs and business objectives
- ✓ Requirements are specific and measurable
- ✓ Acceptance criteria are testable
- ✓ Technical feasibility is validated
- ✓ Success metrics are defined and trackable
- ✓ Risks are identified with mitigation plans
- ✓ Stakeholder alignment is confirmed

## USER STORY EXAMPLE

### Epic: User Authentication System

**Story**: As a new user, I want to create an account with my email so that I can access personalized features.

**Acceptance Criteria:**

- The user can input an email address and password
- The system validates the email format and password strength
- The user receives a confirmation email with a verification link
- The account is created only after email verification
- The user is redirected to the onboarding flow after verification
- Error messages are clear and actionable

**Definition of Done:**

- Functionality works across all supported browsers
- Responsive mobile design implemented
- Security requirements met (encryption, validation)
- Analytics tracking configured
- User testing completed with 90%+ task completion
- Performance meets requirements (load time under 2 seconds)

---

**Remember**: A great PRD balances clarity with flexibility, providing enough detail to guide development while remaining adaptable to new insights.
